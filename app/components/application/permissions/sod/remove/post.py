import os

from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=os.path.dirname(__file__),
)
def remove(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codesod: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    try:
        model_sod: appmodels.ApplicationPermissionsSoD
        try:
            model_sod = appmodels.ApplicationPermissionsSoD.objects.get(  # noqa: E501
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

        permission_sod: str = model_sod.permission_sod
        permission_sod_split = permission_sod.split("_")
        permission1: str = (
            f"{permission_sod_split[0]}_{permission_sod_split[1]}"  # noqa
        )
        permission2: str = (
            f"{permission_sod_split[2]}_{permission_sod_split[3]}"  # noqa
        )

        appmodels.ApplicationPermissionsSoD.objects.filter(
            permission_sod__in=[
                f"{permission1}_{permission2}",
                f"{permission2}_{permission1}",
            ]
        ).delete()

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully removed")
            % {
                "field": "sod",
            },
        )

        return redirect(
            "app:application:permissions:sod:page",
        )

    except ValueError as e:
        if str(e) in ("sod_not_found",):
            return redirect(
                "app:application:permissions:sod:page",
            )

        raise ValueError(e)
