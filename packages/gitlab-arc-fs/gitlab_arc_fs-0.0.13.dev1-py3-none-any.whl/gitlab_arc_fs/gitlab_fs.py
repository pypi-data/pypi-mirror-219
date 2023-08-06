from fs.base import FS
from fs.info import Info
from fs.mode import Mode
from fs.subfs import SubFS
from fs.errors import ResourceNotFound, DirectoryExpected,\
                      ResourceReadOnly, Unsupported, FileExists, FileExpected,\
                      FileExpected, DirectoryExists, ResourceNotFound # NOQA
from fs.permissions import Permissions
from pathlib import Path
import asyncio
import aiohttp
import urllib3 # NOQA
import threading
import os # NOQA
import requests
import io
from hashlib import sha256
import logging

logging.basicConfig(filename="output.log",
                    level=logging.ERROR)


# try:
#     from dotenv import load_dotenv
#     from os import getenv
# except ImportError:
#     pass

try:
    from .lfs_file import LFSFile
except ImportError:
    from lfs_file import LFSFile

try:
    from .gitlab_filestream import FileStreamHandler
except ImportError:
    from gitlab_filestream import FileStreamHandler


class RunThread(threading.Thread):
    """
    Class to run an asynchronus function
    in a new thread.

    Sligthly changed verion of this answer on
    SO:
    https://stackoverflow.com/a/63072524
    Credits to Mark:
    https://stackoverflow.com/users/2606953/mark
    """
    def __init__(self, func, args):
        self.func = func
        self.args = args
        self.result = None
        super().__init__()

    def run(self):
        self.result = asyncio.run(self.func(*self.args))


class GitlabFS(FS):
    """A PyFileSystem2 extension for Gitlab"""

    def __init__(self,
                 token: str,
                 server_url: str):
        super().__init__()
        self.server_url = server_url
        self.hostname = server_url.replace("https://", "")
        self.token = token

        # Create a FileStreamHandler, which manages a lot of the communication
        # with the GitLab server.
        self.fstream = FileStreamHandler(server_url,
                                         token)

        # Remember already accessed repositories to avoid
        # requesting the same repository-tree multiple times.
        self.accesed_repositories = set()

        # Get the initial (toplevel) directory structure.
        # This is essentially a list of directories which represent
        # all Arcs a user has access to with a given token.
        # The repository metadatastructures are constructed, per directory,
        # upon requesting more detailed information about a file in this
        # directory
        self.repo_list = self._get_accessable_repositories()

        # Create a dictionary, which will be used to store information about
        # the repositories.
        # {pathlib.Posixpath(repo_path): dict}
        # dict has (u.a.) the keys: id, description, name, name_with_namespace,
        # path, path_with_namespace, created_at, default_branch,
        # ssh_url_to_repo, http_url_to_repo, last_activity_at.
        # TODO: Maybe change _build_repo_dict to be side effect free.
        self.repos_dictionary = {}
        self._build_repo_dict()

        # Create an empty dictionary, which will be used to store information
        # about the directories and files -inside- a repository.
        # {repo_id: dict[Posixpath(filepath): {"is_dir": bool, "name": str}]}
        # TODO: Also save the date-time for a possible cache update later on.
        self.repo_trees_dict = {}

        # Create a metadata dictionary for all repositories as
        # well as for the root directory ("/"). This information is initially
        # retrieved and provided for the toplevel (view over all repositories).
        # For the directories inside a repository, this information is build
        # lazily for each (sub)directory upon requesting the information of a
        # contained file.
        # {Path: {"info": fs.Info object}
        # Info object contains details about: is_dir, is_file, size, type
        # More information: https://docs.pyfilesystem.org/en/latest/info.html
        self.info_dict = {}
        self._build_initial_repository_info()

    def _build_initial_repository_info(self) -> None:
        """
        Build info from self.repos_dictionary for all accesible repositories
        (toplevel) and save this info in self.info_dict.

        """
        for (path, details) in self.repos_dictionary.items():
            name = path.parts[-1]
            created = details.get('created_at')

            info = {"basic": {"name": name, "is_dir": True},
                    "details": {"accessed": None,
                                "created": created,
                                "metadata_changed": None,
                                "modified": None,
                                "size": None,
                                "type": 1}}
            self.info_dict.update({path: Info(info)})

    def _check_ressource(self, path: str):
        """
        """
        (id, repo) = self._get_repo_id_path(path)
        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, repo)
        if path in self.repo_trees_dict.get(id):
            return True
        return False

    def _build_directory_info(self, path: str) -> None:
        """
        Builds the directory info for a given path, which
        is the path of a directory INSIDE of a repository.
        The metadata information will be collected for all
        files in the directory.
        Will set metadata as self.info_dict[path].
        If path is the path to a file, will raise DirectoryExpected.

        Args:
            path (str): The path to the directory or file
                        to retrieve information about.

        Returns:
            None

        Raises:
            DirectoryExpected: If the path is not a directory.
        """
        if not self.isdir(path):
            if not self._check_ressource(path):
                raise ResourceNotFound(path)
            else:
                raise DirectoryExpected(path)

        # Check if the info of the non-file information
        # (i.e. the directory tree information) of the
        # with path corresponding repository is already build.
        (id, root_path) = self._get_repo_id_path(str(path))
        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, root_path)

        repo_tree = self.repo_trees_dict[id]
        for (pth, raw_info) in repo_tree.items():
            if (str(pth.parent) == path or str(pth) == path)\
                                              and self.isdir(pth):
                name = raw_info.get('name')
                info = {"basic": {"name": name, "is_dir": True},
                        "details": {"accessed": None,
                                    "created": None,
                                    "metadata_changed": None,
                                    "modified": None,
                                    "size": None,
                                    "type": 1}}
                self.info_dict.update({pth: Info(info)})

        # Retrieve information about all files under path.
        raw_info_dict = self.run_async(self._retrieve_metadata, path)
        for (pth, info_raw) in raw_info_dict.items():
            name = info_raw['name']
            size = int(info_raw["size"])
            info = {"basic": {"name": name, "is_dir": False},
                    "details": {"accessed": None,
                                "created": None,
                                "metadata_changed": None,
                                "modified": None,
                                "size": size,
                                "type": 2}}
            self.info_dict.update({pth: Info(info)})

    async def _retrieve_metadata(self, path: str, semaphore: int = None)\
            -> dict:
        """
        This function asynchronously retrieves the (needed) metadata
        by asynchronously sending HTTP-request to the Gitlab-API.

        NOTE: This function should only be called from within
              _build_directory_info.

        Args:
            path (str): The path to the repository / directory to retrieve
                        information about.
            semaphore (int): Number to limit concurrency to.

        Returns:
            paths_info (dict): TODO: Add return details.

        Raises:
            No internal exception handling.
         """
        if semaphore is None:
            semaphore = 10

        if path != "/":
            path = path.strip("/")
        repo_id, repo_path = self._get_repo_id_path(str(path))
        semaphore = asyncio.BoundedSemaphore(semaphore)
        paths = self._gather_file_paths(path)
        urls = [self.fstream.construct_url(
            str(path),
            repo_id,
            repo_path)
            for path in paths]

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(
                self.fstream._get_gitlab_metadata(url,
                                                  path,
                                                  session,
                                                  semaphore))
                     for (url, path) in zip(urls, paths)]
            # asyncio.gather returns a list of return values, maintaining the
            # order (i.e. the return value of the first task inserted in the
            # queue will be the first value in temp, regardless of time of
            # completion)
            temp = await asyncio.gather(*tasks)

        paths_info = {key: value for (key, value) in zip(paths, temp)}

        return paths_info

    def _gather_file_paths(self, path: str) -> list:
        """
        Gather all the paths to (non dir) files in the directory tree,
        which are in the directories specified by path. If path is
        a path to a file, return [path].

        Args:
            path (str): The path to directory or file to gather the paths from.

        Returns:
            directory_list:             A list of paths to (non dir) files
            (list[pathlib.PosixPath])   which lay in the directory
                                        specified by path.

        Raises:
            No internal exception handling.
        """
        # If we are in the root directory, return only the
        # toplevel ARC-View.
        # This information ist stored in self.repos_dictionary.
        if path == "/":
            path_list = [key for key in self.repos_dictionary
                         if key != path]
            return path_list
        else:
            path = path.strip('/')

        path = Path(path)
        # Get the repository id and path.
        # Build the repository tree, if necessary.
        (id, repo_path) = self._get_repo_id_path(str(path))
        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, repo_path)

        # Return path, if path is the path to a file.
        repo_tree = self.repo_trees_dict.get(id)
        if not repo_tree.get(path).get("is_dir"):
            return [path]

        path_list = []
        for path_key in repo_tree:
            parent = path_key.parent
            isdir = repo_tree.get(path_key).get("is_dir")
            if parent == path and not isdir:
                path_list.append(path_key)

        return path_list

    def _get_repo_id_path(self, path: str) -> tuple:
        """
        Returns a tuple containing the ID and repository path of the with
        repository corresonding with path.

        Args:
            path (str): path do a directory or file (inside a repository).

        Returns:
            TODO: check return values inside tuple.
            (ID: int, path: pathlib.Posixpath): A tuple of the repository id
                                                and repository path
                                                corresponding with path.
        """
        # Set alternative root paths names to the root path.
        if path == "." or path == "./":
            path = "/"
        # Remove trailing / leading slash.
        if path != "/":
            path = path.strip("/")
        path = Path(path)
        root_path = path.parts[0]
        try:
            id = self.repos_dictionary.get(Path(root_path)).get("id")
        except (KeyError, AttributeError):
            id = None
            root_path = None
        return (id, root_path)

    def _get_accessable_repositories(self) -> dict:
        """
        Gets information about the repository which are accessible with
        the given token.

        Args: None

        Returns:
            data (dict):   A list of dictionaries containing information about
                           the reposiories.

        Raises:
            SystemExit: if a bad status Code (HTTPError) or a ambigous Request
                        exception is recieved.

        """
        # Maybe Discard all other information besides id, path and
        # is_repository.
        download_url = f"{self.server_url}/api/v4/projects/"
        try:
            with requests.Session() as session:
                r = session.get(download_url,
                                headers={"PRIVATE-TOKEN": self.token},
                                data={"simple": True,
                                      "pagination": "keyset",
                                      "order_by": "id",
                                      "sort": "desc"})
                r.raise_for_status()
        except requests.HTTPError as e:
            print("Bad status code:", r.status_code)
            print("Exiting program")
            raise SystemExit(e)
        except requests.exceptions.Timeout:
            print("Timout error")
            # TODO: Add some retry functionality here.
        except requests.exceptions.RequestException as e:
            print("Recieved ambiugous request exception")
            raise SystemExit(e)

        data = r.json()
        next_references = True

        while next_references:
            try:
                download_url = r.links["next"]["url"]
            except KeyError:
                next_references = False
                session.close()
                continue
            try:
                with requests.Session() as session:
                    r = session.get(download_url,
                                    headers={"PRIVATE-TOKEN":
                                             self.token})
                    r.raise_for_status()
            except requests.HTTPError as e:
                print("Bad status code:", r.status_code)
                print("Exiting program")
                raise SystemExit(e)
            except requests.exceptions.Timeout:
                print("Timout error")
                # TODO: Add some retry functionality here.
            except requests.exceptions.RequestException as e:
                print("Recieved request exception:")
                raise SystemExit(e)
            data.extend(r.json())

        for dict in data:
            # dict["path_without_namespace"] = Path(dict.get("path"))
            path = dict.get("name_with_namespace")
            formated_path = path.replace(" / ", "-").replace(" ", "_")
            dict["path_formated"] = Path(formated_path)
            # dict["path_formated"] = Path(dict.pop("path_with_namespace")
            #                              .replace("/", "-"))
            dict.update({"is_repository": True,
                         "is_dir": True})

        # Adding the root directory.
        data.append({"path_formated": Path("/"),
                     "path": Path("/"),
                     "is_repository": False,
                     "is_dir": True})
        return data

    def _build_repo_dict(self) -> None:
        """
        Construct the directory dict structure from self.repo_list.
        Sets the structure as self.repos_dictionary.

        Args: None
        Returns: None
        Raises: No internal exception handling.
        """
        for el in self.repo_list:
            key = el.get("path_formated")
            value = el
            self.repos_dictionary.update({key: value})

    def _construct_tree_dict(self, repo_id: int,
                             repo_path: str) -> None:
        # TODO: Type annotation
        # TODO: Add datetime
        # TODO: Maybe extract everything with requests to gitlab_filestream
        """
        Builds self.repos_dictionary for a given repository(id).

        Args:
            repo_id (int): ID of the repository fot which the directory tree
                           should be constructed.

            path (str):    Path of the directory for prefixing of the
                           directory paths.

        Returns:
            None

        Raises:
            SystemExit: If a RequestError or HTTPError occured.
        """
        # Get the repotree.
        download_url = (f"{self.server_url}/api/v4/projects/"
                        f"{repo_id}"
                        f"/repository/tree")

        # Set the pagination method to keyset, to retrieve the total number of
        # pages. For more information about pagination, see
        # https://docs.gitlab.com/ee/api/repositories.html and
        # https://docs.gitlab.com/ee/api/index.html#keyset-based-pagination
        # In short: This is necessary because all files in the repository will
        # be needed.
        try:
            r = requests.get(download_url,
                             headers={"PRIVATE-TOKEN": self.token},
                             data={"recursive": True,
                                   "pagination": "keyset",
                                   "order_by": "id",
                                   "sort": "asc",
                                   "per_page": 100})
            r.raise_for_status()
        except requests.HTTPError as e:
            print("Bad status code:", r.status_code)
            print("Exiting program")
            raise e
        except requests.exceptions.Timeout:
            print("Timout error")
            # TODO: Add some retry functionality here.
        except requests.exceptions.RequestException as e:
            print("Recieved request exception")
            print("Exiting program")
            raise SystemExit(e)

        # This could possibly be done asynchronously, but
        # the Gitlab API suggests using the URLs contained in
        # the headers instead of constructing URLs.
        num_pages = int(r.headers["x-total-pages"])

        # tree is a now list of dictionaries, one for each
        # ressource in a agiven repository with, the keys
        # "id", "name", "type", "path" and "mode".
        tree = r.json()

        # Get the repo tree for all files in the repository.
        # This is done by following the links specified in the
        # response. One for each following page.
        for i in range(num_pages-1):
            download_url = r.links["next"]["url"]
            try:
                r = requests.get(download_url,
                                 headers={"PRIVATE-TOKEN":
                                          self.token})
                r.raise_for_status()
            except requests.HTTPError as e:
                print("Bad status code:", r.status_code)
                print("Exiting program")
                raise SystemExit(e)
            except requests.exceptions.Timeout:
                print("Timout error")
                # TODO: Add some retry functionality here.
            except requests.exceptions.RequestException as e:
                print("Recieved request exception:")
                raise SystemExit(e)
            tree.extend(r.json())

        # tree is a list of dictionaries with the keys
        # "id", "name", "type", "path" and mode.
        # Convert list to a dictionary.
        directory_dict = {}
        for element in tree:
            # Prefixing the path with the repository name/path
            path = Path(repo_path, element.get('path'))
            is_dir = True if element.get('type') == 'tree' else False
            info = {"is_dir": is_dir, "name": element.get('name')}
            directory_dict.update({path: info})

        # Also insert the root directory of the repository.
        name = repo_path
        repo_path = Path(repo_path)
        info = {"is_dir": True, "name": name}
        directory_dict.update({repo_path: info})

        self.repo_trees_dict.update({repo_id: directory_dict})
        self.accesed_repositories.add(repo_id)

    def getinfo(self, path: str, namespaces=None) -> Info:
        """
        TODO: Docstings
        """
        if path in [".", "./", ""]:
            path = "/"
        if path != "/":
            path = path.strip("/")

        # Ceck if the given path is a path to a repository.
        # If so, the metadata information is already available
        # in self.info_dict.
        if self.isrepository(path):
            try:
                return self.info_dict[Path(path)]
            except KeyError:
                raise ResourceNotFound(path)

        # Check in the repository corresponding to the path
        # was already accessed.
        (id, repo_path) = self._get_repo_id_path(str(path))
        if id not in self.accesed_repositories:
            try:
                self._construct_tree_dict(id, repo_path)
            except requests.exceptions.HTTPError:
                raise ResourceNotFound(path)

        # Check if metadata for the given path is available already.
        path = Path(path)
        info = self.info_dict.get(path)
        # If not, retrieve the metadata for all files in the given path.
        # If path is the path to a file, then for all files in the same
        # directory
        if info is None:
            if self.isdir(path):
                raw_info = self.repo_trees_dict[id][Path(path)]
                name = raw_info.get('name')
                info = {"basic": {"name": name, "is_dir": True},
                        "details": {"accessed": None,
                                    "created": None,
                                    "metadata_changed": None,
                                    "modified": None,
                                    "size": None,
                                    "type": 1}}
                self.info_dict.update({path: Info(info)})
            else:
                # Maybe check here if the partent path is a repo
                self._build_directory_info(str(path.parent))
        # If the metadata for path is nit in self.info_dict,
        # then the resource was not found.
        try:
            return self.info_dict[path]
        except KeyError:
            raise ResourceNotFound(path)

    def listdir(self, path: str) -> list:
        """
        Get a list of the resource names in a directory.
        This method will return a list of the resources in a directory.

        Arguments:
            path (str):     A path to a directory on the filesystem

        Returns:
            directory_list (list): list of names, relative to path.

        Raises:
            fs.errors.DirectoryExpected: If ``path`` is not a directory.
            fs.errors.ResourceNotFound: If ``path`` does not exist.
        """
        # Set alternative root paths names to the root path.
        if path == "." or path == "./":
            path = "/"
        # Remove trailing / leading slash.
        if path != "/":
            path = path.strip("/")

        directory_list = []

        # handling of the top-level directory (the view on different ARCs)
        if path == "/":
            directory_list = [str(repo.get("path_formated"))
                              for repo in self.repo_list
                              if repo.get("id") is not None]
            return directory_list

        # Get the root directory of the given path (which will be an
        # repository). Get the repository id. With this, check if the
        # given path is already in self.repos_dictionary.
        # If not, try to build it.
        is_repository = self.isrepository(path)
        (id, root_path) = self._get_repo_id_path(str(path))

        # If the root path is not in self.repos_dictionary, it can't be
        # a repository which the user has acces to.
        if id is None:
            raise ResourceNotFound(path)
        # Check if the repository described by root path was already build.
        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, root_path)

        # Check if the path is a valid directory or repository
        # TODO: Revisit this after getinfo and isdir are implemented.
        if (self.repo_trees_dict.get(id).get(Path(path)) is None and
           is_repository is False):
            raise ResourceNotFound(path)
        # Check if the path is a directory.
        if not is_repository:
            if not self.isdir(str(path)):
                raise DirectoryExpected(path)

        paths_list = [path for path in self.repo_trees_dict.get(id)]
        directory_list = [pth.name for pth in paths_list
                          if pth.parent == Path(path)]

        return directory_list

    def isrepository(self, path: str) -> bool:
        """
        TODO: Docstings
        """
        if path in [".", "./", ""]:
            path = "/"
        if path != "/":
            path = path.strip('/')
        root_path = Path(path).parts[0]
        is_repository = False
        if root_path == path:
            is_repository = True
        return is_repository

    def isdir(self, path: str) -> bool:
        """
        Check if a path maps to an existing directory.

        Arguments:
            path (str): A path on the filesystem.

        Returns:
            bool: `True` if ``path`` maps to a directory.

        """
        # Set alternative root paths names to the root path.
        if path in [".", "./", ""]:
            path = "/"
        path = Path(path)
        # Check if the path is a repository (and therefore a directory).
        if path in self.repos_dictionary:
            return True
        # Check if the repository corresponding to the given path is
        # already build.
        (id, root_path) = self._get_repo_id_path(str(path))
        # If the root path is not in self.repos_dictionary, it can't be
        # a repository which the user has access to. So in this case,
        # the resource is not a found and therefore not a dictionary.
        if id is None:
            return False

        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, root_path)

        repo_tree = self.repo_trees_dict.get(id)
        if path not in repo_tree:
            return False

        if repo_tree.get(path).get("is_dir"):
            return True

        return False

    def openbin(self, path: str, mode='r', buffering=-1, **options)\
            -> io.IOBase:
        """
        Returns a file like object that can be opened.
        Args:
            path (str): The path to open.
            mode (str): The mode to open the file with. Only read is supported.
            buffering: -
        Returns:
            resp (resp.Response): A Response object for a filestream.
        Raises: No internal exception handling.
        TODO: Possibly implement buffering
        TODO: Improve error handling. Maybe get inspired from one of the
              built-in filesystems.
              See https://github.com/PyFilesystem/fs.dropboxfs
        """
        with self._lock:
            try:
                parsedMode = Mode(mode)
                parsedMode.validate_bin()
            except ValueError as e:
                raise e
            if path != "/":
                path = path.strip("/")
            if self.isdir(path):
                raise FileExpected(path)
            if parsedMode.reading:
                (repo_id, repo_path) = self._get_repo_id_path(str(path))
                r = self.fstream.get_file_stream(path, repo_id, repo_path)
                return r.raw
            if parsedMode.exclusive or parsedMode.writing or parsedMode.create:
                if not parsedMode.exclusive and self._check_ressource(path):
                    raise FileExists(path)
                repo_id, repo_path = self._get_repo_id_path(str(path))
                namespace = self._get_namespace(repo_path)
                path = "/".join(part for part in Path(path).parts[1:])
                path = Path(path)
                if len(path.suffixes) > 1:
                    if path.suffixes[0] == path.suffixes[1]:
                        suffix = path.suffixes[1]
                        path = Path(path.stem)
                        path = path.with_suffix(suffix)

                file = LFSFile(str(path),
                               self.token,
                               self.hostname,
                               namespace,
                               repo_id)
                return file
            else:
                raise Unsupported

    def run_async(self, func, *args):
        """
        TODO: Docstrings
        TODO: return values
        Sligthly changed verion of this answer on
        SO:
        https://stackoverflow.com/a/63072524
        Credits to Mark:
        https://stackoverflow.com/users/2606953/mark
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            thread = RunThread(func, args)
            thread.start()
            thread.join()
            return thread.result
        else:
            return asyncio.run(func(*args))

    def _get_namespace(self, path: str):
        """_summary_

        Args:
            path (str): path to a directory root.
        """
        namespace = self.repos_dictionary.get(Path(path))\
            .get("path_with_namespace")
        return namespace

    def upload(self,
               path: str,
               file,
               chunk_size: int = None,
               ref: str = None,
               **options):
        """Set a file to the contents of a binary file object.

        This method copies bytes from an open binary file to a file on
        the filesystem. This is done by uploading the file as LFS file,
        into a new branch and subsequently creates a merge request into
        the branch specified by ref. Into the deflault branch if ref is
        None.

        Arguments:
            path (str): A path on the filesystem.
            file (io.IOBase): a file object open for reading in
                binary mode.
            chunk_size (int, optional): Number of bytes to read at a
                time, if a simple copy is used, or `None` to use
                sensible default.
            ref (str, optional): The destionation branch of the issued merge
                                 request.
            **options: Implementation specific options required to open
                the source file.

        Raises:
            fs.errors.ResourceNotFound: If a parent directory of
                ``path`` does not exist.

            fs.errors.FileExists: If the file already exists.

        Note that the file object ``file`` will *not* be closed by this
        method. Take care to close it after this method completes
        (ideally with a context manager).

        Example:
            >>> with open('~/movies/starwars.mov', 'rb') as read_file:
            ...     my_fs.upload('starwars.mov', read_file)

        """
        logging.debug(f"In Upload with path: {path}\n")
        with self._lock:
            parent_dir = Path(path).parents[0]

            if not self.isdir(parent_dir):
                raise ResourceNotFound(path)
            if self._check_ressource(path):
                raise FileExists(path)

            repo_id, repo_path = self._get_repo_id_path(path)

            repo_ref = FileStreamHandler._get_default_branch(repo_id,
                                                             self.token,
                                                             self.server_url)\
                if ref is None else ref

            info = self._compute_size_sha(file)
            namespace = self._get_namespace(repo_path)
            branch = LFSFile._create_branch(self.token, repo_ref, repo_id)
            sha256sum = info['shasum'].hexdigest()

            if chunk_size is None:
                chunk_size = 4096

            lfs_object_request_json = {
                "operation": "upload",
                "objects": [
                    {
                        "oid": f"{sha256sum}",
                        "size": f"{info['size']}"
                    }
                ],
                "transfers": [
                    "lfs-standalone-file",
                    "basic"
                ],
                "ref": {
                    "name": "refs/heads/" + repo_ref
                },
                "hash_algo": "sha256"
            }

            headers = {'Accept': 'application/vnd.git-lfs+json',
                       'Content-type': 'application/vnd.git-lfs+json'}

            # construct the download URL for the lfs resource
            download_url = "".join([
                "https://oauth2:",
                f"{self.token}",
                f"@{self.hostname}/",
                f"{namespace}.git/info/lfs/objects/batch"
            ])

            r = requests.post(download_url, json=lfs_object_request_json,
                              headers=headers)
            res = r.json()

            try:
                header_up = res["objects"][0]["actions"]["upload"]["header"]
                url_upload = res["objects"][0]["actions"]["upload"]["href"]
                header_up.pop("Transfer-Encoding")
                file.seek(0, 0)
                res = requests.put(url_upload,              # NOQA
                                   headers=header_up,
                                   data=iter(lambda: file.read(4096*4096),
                                             b""))
                # Almost certainly, the LFS-File was already uploaded. in this
                # case, just update the pointer file and create a merge request
            except KeyError:
                pass

            path = "/".join(part for part in Path(path).parts[1:])
            path_sanitized = self.clean_file_ext(path)
            LFSFile._commit_pointer_file(path_sanitized, info["shasum"],
                                         repo_id, self.token,
                                         info["size"], branch)

            path = "/".join(part for part in Path(path).parts[1:])
            path = Path(path)
            LFSFile._modify_gitattributes(repo_id, self.token, ref, path)
            LFSFile._create_merge_request(repo_id, self.token,
                                          repo_ref, branch)

    def makedir(self, path: str, permissions: Permissions = None,
                recreate: bool = False):
        """TODO: Wreite verbose summery here, especially a Note about the
        "phantom" creation of firectories.

        Args:
            path (str): _description_
            permissions (Permissions, optional): _description_.
                                                 Defaults to None.
            recreate (bool, optional): _description_. Defaults to False.

        Raises:
            fs.errors.DirectoryExists: If the path already exists.
        """
        with self._lock:
            if self.isdir(path):
                if not recreate:
                    raise DirectoryExists
                else:
                    # If we want to recreate a directory, we will just
                    # do nothing, since "recreating" is no specified further.
                    # There will be an error or something however, if a already
                    # present file is attempted to be uploaded.
                    pass
            # Insert the new directory into the appropriate dictionary.
            # After this isdir() will be True.
            # NOTE: On GitLab istself, this will not change anything.
            path = Path(path)
            name = path.parts[-1]
            infos = {path: {"is_dir": True, "name": name}}
            path = str(path)
            (repo_id, repo_path) = self._get_repo_id_path(path)
            repo_dict = self.repo_trees_dict.get(repo_id)
            repo_dict.update(infos)

            return SubFS(self, path)

    def remove():
        raise Unsupported

    def removedir():
        raise Unsupported

    def setinfo():
        raise Unsupported

    @staticmethod
    def clean_file_ext(path: str):
        """_summary_

        Args:
            path (str): _description_

        Returns:
            _type_: _description_
        """
        path = Path(path)
        suffixes = list(dict.fromkeys(path.suffixes))
        while path.suffix:
            path = path.with_suffix("")
        path = path.with_suffix("".join(suffixes))

        return str(path)

    @staticmethod
    def _compute_size_sha(file: io.IOBase):
        """_summary_

        Args:
            file (io.IOBase): _description_
        """
        shasum = sha256()
        file.seek(0)
        for chunk in iter(lambda: file.read(1024*1024*10), b''):
            shasum.update(chunk)
        file.seek(0, 2)

        filesize = file.tell()

        info = {"size": filesize,
                "shasum": shasum}
        file.seek(0)
        return info
