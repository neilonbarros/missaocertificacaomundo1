from typing import Any

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import components as appccomponents
from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=__file__,
)
def page(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    form_sod: appforms.ApplicationPermissionsSoD

    save_sod = request.session.get("SOD_SAVE", None)
    if save_sod is not None:
        del request.session["SOD_SAVE"]
        form_sod = appforms.ApplicationPermissionsSoD(
            data=save_sod,
        )
        form_sod.is_valid()

    else:
        form_sod = appforms.ApplicationPermissionsSoD()

    permissions: list[str] = []

    for x in appccomponents.application.permissions.code.get.permissions:
        permission: str = f"{x['nivel1']}_{x['nivel2']}"

        if permission not in permissions:
            permissions.append(permission)

    model_sods = appmodels.ApplicationPermissionsSoD.objects.all()

    sods: list[dict[str, Any]] = []

    # {
    #     "id": 0,
    #     "permissao1": "xxx",
    #     "permissao2": "xxx",
    # }

    for row in model_sods:
        permission_sod_split = row.permission_sod.split("_")
        permission1: str = (
            f"{_(permission_sod_split[0])}_{_(permission_sod_split[1])}"  # noqa
        )
        permission2: str = (
            f"{_(permission_sod_split[2])}_{_(permission_sod_split[3])}"  # noqa
        )
        sods.append(
            {
                "id": row.id,
                "permission1": permission1,
                "permission2": permission2,
            }
        )

    title: str = "SoD"

    return render(
        request=request,
        template_name="app/application/permissions/sod/_page.html",
        context={
            "settings_debug": settings.DEBUG,
            "sessionuser": session_user,
            "html_language": translation.get_language(),
            "title": title,
            "menu": True,
            "display_center": False,
            "options": "app/application/permissions/sod/options/_page.html",  # noqa
            "form_sod": form_sod,
            "permissions": permissions,
            "sods": sods,
        },
    )
