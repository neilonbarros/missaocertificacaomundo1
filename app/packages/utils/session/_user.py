from typing import Any, Optional


class User(object):
    id: Optional[int] = None
    fullname: str = ""
    password_attempts: int = 3

    def load(self, session: dict[str, Any]) -> None:
        self.id = session.get("id", None)
        self.fullname = session.get("fullname", None)
        self.password_attempts = session.get("password_attempts", None)
