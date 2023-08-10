from rich import print

from app import packages as apppackages
from django.conf import settings
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_control


def validate(
    file: str = "",
):
    def decorator(function):
        @cache_control(
            no_cache=True,
            must_revalidate=True,
            no_store=True,
        )
        def wrapper(
            *args,
            **kwargs,
        ):
            request: HttpRequest = args[0]  # type: ignore
            type_page: str = kwargs.get("type_page", None)  # type: ignore

            with_permission: bool = False  # type: ignore
            session_user: apppackages.utils.Session  # type: ignore

            if kwargs.get("session_user", None) is None:
                session_user = kwargs.get("session_user")  # type: ignore

            else:
                session_user = apppackages.utils.Session(request=request)

            if len(session_user.permissions.type) > 0:
                directories: list[str] = file.split("/")  # type: ignore

                if 'app' not in directories:
                    raise RuntimeError("permissions without map")

                appdir: int = 0  # type: ignore
                for x in range(1, 10):
                    index: int = x * -1  # type: ignore
                    if directories[index] == 'app':
                        appdir = index + 1
                        break

                current_directorie: str = directories[-2]  # type: ignore

                nivel: str = ""  # type: ignore
                permission: str = ""  # type: ignore

                for x in range(1, 11):
                    if x > 1:
                        permission = f"{permission}_"

                    directorie: str = directories[appdir + x]  # type: ignore # noqa: E501
                    permission = f"{permission}{directorie}"

                    if directorie == current_directorie:
                        nivel = f"nivel{str(x)}"
                        break

                if settings.DEBUG is True:
                    print(
                        [
                            nivel,
                            type_page,
                            permission,
                        ]
                    )  # noqa: E501

                if permission in getattr(session_user.permissions, nivel):
                    if type_page is None:
                        with_permission = True

                    elif f"{permission}:{type_page}" in getattr(
                        session_user.permissions, "type"
                    ):  # noqa: E501
                        with_permission = True

            if with_permission is False:
                raise PermissionDenied()

            else:
                return function(*args, **kwargs)

        return wrapper

    return decorator
