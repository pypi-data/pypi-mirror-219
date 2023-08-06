import requests
import urllib
from hashlib import sha256
from datetime import datetime
import io  # NOQA
from json import JSONDecodeError

try:
    from .gitlab_filestream import FileStreamHandler
except ImportError:
    from gitlab_filestream import FileStreamHandler


class LFSFile_2(io.FileIO):
    """
    A class representing a Gitlab LFS file ressource.
    """
    def __init__(self,
                 path: str,
                 token: str,
                 host: str,
                 namespace: str,
                 repo_id: str,
                 local_path: str,
                 ref: str = None):
        """
        Constructor for the LSF file class.

        Args:
            path (str):         The path to the ressource on Gitlab inside a
                                repository.
            token (str):        A Gitlab access token with the scope "API".
            host (str):         Hostname of the GitLab serer
            namespace (str):    The "path" to the repository on GitLab
            repo_id (str):      The id of the repository on GitLab
            local_path:         Path of a local file to be uploaded.
            ref:                The commit-sha / branch name / tag of the
            (str, optional):    repository to use. Defaults to "main".
        """
        super().__init__(file=local_path,
                         mode="wb")
        # self.local_path = local_path

        self.path = path
        self.token = token
        self.host = host
        self.namespace = namespace
        self.repo_id = repo_id

        # Create a sha256 Object to compute the SHAsum during writing into
        # the file. This is necessary for uploading an LFS file.
        self.shasum = sha256()

        # Get the default branch.
        server_url = "https://" + self.host
        sh = FileStreamHandler(server_url, self.token)
        self.ref = sh._get_default_branch(self.repo_id) if ref is None else 