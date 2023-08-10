from typing import Any, Optional


class User(object):
    id: Optional[int] = None
    fullname: str = ""

    def load(self, session: dict[str, Any]) -> None:
        self.id = session.get("id", None)
        self.fullname = session.get("fullname", None)
