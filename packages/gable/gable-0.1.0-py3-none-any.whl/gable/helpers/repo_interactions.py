import os
from typing import Optional, TypedDict
from git.repo import Repo
import giturlparse
from urllib.parse import urljoin


class GitInfo(TypedDict):
    gitHash: str
    gitRepo: str
    gitSSHRepo: str
    gitUser: Optional[str]
    mergedAt: str
    localRepoDir: str


def get_git_info() -> GitInfo:
    repo = Repo(".", search_parent_directories=True)
    parsed_repo = giturlparse.parse(repo.remotes.origin.url)
    return {
        "gitHash": repo.head.commit.hexsha,
        "gitRepo": repo.remotes.origin.url,
        "gitSSHRepo": parsed_repo.url2ssh.rstrip(".git"),
        "gitUser": repo.head.commit.author.name,
        "mergedAt": repo.head.commit.committed_datetime.isoformat(),
        "localRepoDir": repo.git_dir,
    }


def get_git_ssh_file_path(git_info: GitInfo, local_file_path):
    absolute_file_path = os.path.abspath(local_file_path)
    relative_path = absolute_file_path.replace(
        git_info["localRepoDir"].replace(".git", ""), "", 1
    )
    return urljoin(git_info["gitSSHRepo"], relative_path)
