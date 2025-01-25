from typing import Any
from typing import Callable
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_get_repo_by_name_success(build_github_customer: Callable[..., Any]):
    mock_response = {
        "items": [
            {
                "id": 1,
                "name": "test-repo",
                "full_name": "owner/test-repo",
                "html_url": "https://github.com/owner/test-repo",
                "description": "A test repository",
                "stargazers_count": 100,
                "forks_count": 50,
                "language": "Python",
                "owner": {
                    "login": "owner",
                    "avatar_url": "https://avatars.githubusercontent.com/u/12345678?v=4",
                },
            }
        ]
    }
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        github_customer = build_github_customer()
        result = await github_customer.get_repo_by_name("test-repo")
        assert await result == mock_response
        mock_get.assert_called_once_with(
            "https://api.github.com/search/repositories",
            headers={"Accept": "application/vnd.github.v3+json"},
            params={"q": "test-repo", "per_page": 5, "page": 1},
        )


@pytest.mark.asyncio
async def test_get_user_repositories_success(build_github_customer: Callable[..., Any]):
    mock_response = [
        {
            "id": 1,
            "name": "repo1",
            "full_name": "owner/repo1",
            "html_url": "https://github.com/owner/repo1",
            "description": "Repository 1",
            "stargazers_count": 10,
            "forks_count": 5,
            "language": "Python",
            "owner": {
                "login": "owner",
                "avatar_url": "https://avatars.githubusercontent.com/u/12345678?v=4",
            },
        },
        {
            "id": 2,
            "name": "repo2",
            "full_name": "owner/repo2",
            "html_url": "https://github.com/owner/repo2",
            "description": "Repository 2",
            "stargazers_count": 20,
            "forks_count": 10,
            "language": "JavaScript",
            "owner": {
                "login": "owner",
                "avatar_url": "https://avatars.githubusercontent.com/u/12345678?v=4",
            },
        },
    ]

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        github_customer = build_github_customer()
        result = await github_customer.get_user_repositories("owner")
        assert await result == mock_response
        mock_get.assert_called_once_with(
            "https://api.github.com/users/owner/repos",
            headers={"Accept": "application/vnd.github.v3+json"},
            params=None,
        )
