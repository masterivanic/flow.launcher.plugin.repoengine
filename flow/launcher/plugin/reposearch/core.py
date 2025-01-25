from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Optional


class RepoSearchCustomer(ABC):
    @abstractmethod
    async def get_repo_by_name(self, repo_name: str = None) -> Optional[Dict]:
        pass

    @abstractmethod
    async def get_user_repositories(self, owner: str = None) -> Optional[List[Dict]]:
        pass
