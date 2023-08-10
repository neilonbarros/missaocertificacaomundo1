from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.decorators.cache import cache_control
from rich import print


def not_authenticated():
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
            user: dict[str, Any] = request.session.get("user", None)  # type: ignore # noqa: E501

            if settings.DEBUG is True:
                print(__file__)
                print(request.session.__dict__)

            if user is not None:
                return redirect("app:home:page")

            else:
                return function(*args, **kwargs)

        return wrapper

    return decorator
