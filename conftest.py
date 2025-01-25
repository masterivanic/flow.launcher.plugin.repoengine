from typing import Any
from typing import Callable

import pytest

from flow.launcher.plugin.reposearch.github_api import GitHubCustomer


@pytest.fixture(scope="function")
def build_github_customer() -> Callable[..., Any]:
    def _build_github_customer(token=None):
        return GitHubCustomer(token=token)

    return _build_github_customer
