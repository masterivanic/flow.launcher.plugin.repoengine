import asyncio
import os
import re
import sys
from typing import Any
from typing import List
from typing import Type

from flowlauncher import FlowLauncher

from flow.launcher.plugin.reposearch.github_api import GitHubCustomer
from flow.launcher.plugin.reposearch.utils.github import GithubObj

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))


class RepoSearchEngine(FlowLauncher):
    SEARCH_REPO_FROM_GIT_COMMAND = "repo git-repo"
    SEARCH_REPO_FROM_GIT_BY_OWNER_COMMAND = "repo git-owner"

    list_url: List[str] = []

    def __init__(self, customer: Type[GitHubCustomer | Any]):
        super().__init__()
        self.customer = customer

    def is_query_format_as_well(self, query: str) -> bool:
        patterns = (
            rf"^{self.SEARCH_REPO_FROM_GIT_COMMAND} \S+$",
            rf"^{self.SEARCH_REPO_FROM_GIT_BY_OWNER_COMMAND} \S+$",
        )
        return any(bool(re.match(pattern, query)) for pattern in patterns)

    def add_repo_url(self, repo_obj: Type[GithubObj | Any]):
        self.list_url.append(repo_obj.flowMessage())

    def query(self, query: str = "repo git-repo hello-world"):
        # TODO: make a decorator to this function to be less
        response = []
        query = query.strip("")
        loop = asyncio.get_event_loop()
        if self.is_query_format_as_well(query=query):
            if self.SEARCH_REPO_FROM_GIT_COMMAND in query:
                response = loop.run_until_complete(
                    self.customer.get_repo_by_name(
                        query.replace(self.SEARCH_REPO_FROM_GIT_COMMAND, "").strip("")
                    )
                )
                response = [GithubObj(obj) for obj in response["items"]]
            elif self.SEARCH_REPO_FROM_GIT_BY_OWNER_COMMAND in query:
                response = loop.run_until_complete(
                    self.customer.get_user_repositories(
                        query.replace(
                            self.SEARCH_REPO_FROM_GIT_BY_OWNER_COMMAND, ""
                        ).strip("")
                    )
                )
                response = [GithubObj(obj) for obj in response]
            for gitobj in response:
                self.add_repo_url(gitobj)
        else:
            raise Exception("Unknow command, verify command guide")


if __name__ == "__main__":
    github_customer = GitHubCustomer()
    RepoSearchEngine(customer=github_customer)
