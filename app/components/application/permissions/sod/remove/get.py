import os

from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=os.path.dirname(__file__),
)
def page(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codesod: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    try:
        try:
            appmodels.ApplicationPermissionsSoD.objects.get(  # noqa: E501
                id=codesod,
            )

        except appmodels.ApplicationPermissionsSoD.DoesNotExist:
            djangomessages.error(
                request=request,
                message=_("%(field)s not found")
                % {
                    "field": "sod",
                },
            )
            raise ValueError("sod_not_found")

        title: str = f"SoD {_('remove')}"

        return render(
            request=request,
            template_name="app/application/permissions/sod/remove/_page.html",  # noqa
            context={
                "settings_debug": settings.DEBUG,
                "sessionuser": session_user,
                "html_language": translation.get_language(),
                "title": title,
                "menu": False,
                "display_center": True,
                "codesod": codesod,
                "type_page": type_page,
            },
        )

    except ValueError as e:
        if str(e) in ("sod_not_found",):
            return redirect(
                "app:application:permissions:sod:page",
            )

        raise ValueError(e)
