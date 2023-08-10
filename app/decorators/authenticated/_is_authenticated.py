from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils import timezone as djangotimezone
from django.views.decorators.cache import cache_control
from rich import print

from app import packages as apppackages


def is_authenticated():
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

            if settings.DEBUG is True:
                print(__file__)
                print(request.session.__dict__)

            if request.session.get("user", None) is None:
                return redirect("app:signin:page")

            else:
                session_user: apppackages.utils.Session  # type: ignore
                session_user = apppackages.utils.Session(request=request)

                if session_user.lifetime < djangotimezone.now().date():
                    del request.session["user"]
                    return redirect("app:signin:page")

                else:
                    if kwargs.get("session_user", None) is None:
                        kwargs.update({"session_user": session_user})
                    return function(*args, **kwargs)

        return wrapper

    return decorator
