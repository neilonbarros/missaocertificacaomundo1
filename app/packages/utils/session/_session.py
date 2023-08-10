from datetime import date
from typing import Any

from django.http import HttpRequest
from django.utils import timezone as djangotimezone

from ._permissions import Permissions
from ._user import User


class Session:
    exists: bool = False
    lifetime: date
    user: User = User()
    permissions: Permissions = Permissions()

    def __init__(self, request: HttpRequest) -> None:
        session_user: dict[str, Any] = request.session.get("user", None)
        if session_user is not None:
            self.exists = True

            lifetime = session_user.get("lifetime", None)
            if lifetime is not None:
                self.lifetime = (
                    djangotimezone.now()
                    .strptime(
                        lifetime,
                        "%Y-%m-%d",
                    )
                    .date()
                )

            self.user = User()
            self.user.load(session=session_user)
            self.permissions = Permissions()
            self.permissions.load(session=session_user)

    def save(self) -> dict[str, Any]:
        user: dict[str, dict[str, Any]] = {
            "user": {
                "lifetime": self.lifetime.strftime("%Y-%m-%d"),
                "id": self.user.id,
                "name": self.user.fullname,
                "permissions": self.permissions.get(),
            },
        }

        return user
