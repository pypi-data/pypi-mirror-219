"""Defines the GitlabFS opener."""

__all__ = ['GitlabFSOpener']

import urllib
import fs # NOQA

from fs.opener import Opener
from fs.opener.errors import OpenerError # NOQA
from fs.base import FS

try:
    from .gitlab_fs import GitlabFS
except ImportError:
    from gitlab_arc_fs import GitlabFS # NOQA


class GitlabFSOpener(Opener):
    """
    The Gitlab FSOpener class represents a gitlab_arc_fs fsopener.
    TODO: Implement error handling.
    """
    protocols = ['arcfs']

    def open_fs(self, fs_url, parse_result, writeable=True,
                create=True, cwd=None) -> FS:
        private_token = parse_result.username
        print(parse_result)

        url = urllib.parse.urlparse(parse_result.resource)
        server_url = url.scheme + '://' + url.netloc

        return GitlabFS(private_token, server_url)
