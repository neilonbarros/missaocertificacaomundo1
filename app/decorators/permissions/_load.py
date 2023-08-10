from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_control
from rich import print

from app import packages as apppackages


def load(
    model_permissions,
    model_peoples,
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
            session_user: apppackages.utils.Session  # type: ignore

            if settings.DEBUG is True:
                print(__file__)
                print(request.session.__dict__)

            if kwargs.get("session_user", None) is None:
                session_user = kwargs.get("session_user")  # type: ignore

            else:
                session_user = apppackages.utils.Session(request=request)

            if session_user.exists is False or session_user.user.id is None:
                if session_user.user.id is None:
                    del request.session["user"]
                    request.session.modified = True
                return redirect("app:signin:page")

            else:
                try:
                    peoples_model = model_peoples.objects.get(
                        id=session_user.user.id,
                    )

                    result_permissions = model_permissions.objects.filter(  # noqa: E501
                        jobposition=peoples_model.jobposition,
                    )

                    session_user.user.id = peoples_model.id
                    session_user.user.fullname = peoples_model.fullname
                    session_user.permissions.update(
                        result_permissions=result_permissions,
                    )

                    if settings.DEBUG is True:
                        print(__file__)
                        print(session_user.permissions.__dict__)

                    request.session.update(session_user.save())
                    request.session.modified = True

                    kwargs.update({"session_user": session_user})  # type: ignore # noqa: E501

                except model_peoples.DoesNotExist:
                    del request.session["user"]
                    message = _("no permission")
                    djangomessages.error(
                        request=request,
                        message=message,
                    )
                    return redirect("app:signin:page")

            return function(*args, **kwargs)

        return wrapper

    return decorator
