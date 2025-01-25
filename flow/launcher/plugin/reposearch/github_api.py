from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import httpx

from flow.launcher.plugin.reposearch.core import RepoSearchCustomer


class GitHubCustomer(RepoSearchCustomer):
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    async def _make_request(
        self, endpoint: str, params: Dict[str, Any] = None
    ) -> Optional[Dict]:
        """NOTE: requests with limit to 60 requests per hour for unauthenticated user"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    endpoint, headers=self.headers, params=params
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None

    async def get_repo_by_name(self, repo_name: str) -> Optional[Dict]:
        endpoint = f"{self.base_url}/search/repositories"
        params = {"q": repo_name, "per_page": 5, "page": 1}
        return await self._make_request(endpoint=endpoint, params=params)

    async def get_user_repositories(self, owner) -> Optional[List[Dict]]:
        endpoint = f"{self.base_url}/users/{owner}/repos"
        return await self._make_request(endpoint=endpoint)
