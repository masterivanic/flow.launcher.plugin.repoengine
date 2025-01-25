from typing import Any
from typing import Dict


class GithubObj(object):
    def __init__(self, **data):
        self.data = data
        if not isinstance(data, dict):
            raise Exception("github format response change")

        self._name = data.get("name", None)
        self._full_name = data.get("full_name", None)
        self._repo_url = data.get("html_url", None)
        self._created_at = data.get("created_at", None)
        self._language = data.get("language", None)
        self._topics = data.get("topics", list())

    @property
    def name(self) -> str:
        return self._name

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def repo_url(self) -> str:
        return self._repo_url

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def language(self) -> str:
        return self._language

    @property
    def topics(self) -> str:
        return self._topics

    def flowMessage(self) -> Dict[str, Any]:
        return {
            "Title": self.full_name,
            "SubTitle": self.full_name + "🚀" + self.created_at,
            "IcoPath": "Images/app.png",
        }
