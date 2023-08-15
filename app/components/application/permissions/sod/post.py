from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=__file__,
)
def save(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    try:
        form_sod: appforms.ApplicationPermissionsSoD
        form_sod = appforms.ApplicationPermissionsSoD(
            data=request.POST,
        )

        if form_sod.is_valid() is False:
            print(form_sod.errors.as_json())
            djangomessages.error(
                request=request,
                message=_("there are fields to check"),
            )
            raise ValueError("form_is_not_valid")

        form_cleaned_data = form_sod.cleaned_data
        permission1: str = form_cleaned_data["permission1"]
        permission2: str = form_cleaned_data["permission2"]

        sod1_description: str = f"{permission1}_{permission2}"
        sod2_description: str = f"{permission2}_{permission1}"

        try:
            appmodels.ApplicationPermissionsSoD.objects.get(
                permission_sod=sod1_description
            )

            djangomessages.error(
                request=request,
                message=_("%(field)s already exists")
                % {
                    "field": "sod",
                },
            )

            raise ValueError("sod_already_exists")

        except appmodels.ApplicationPermissionsSoD.DoesNotExist:
            list_model_sods: list[appmodels.ApplicationPermissionsSoD]

            sod1: appmodels.ApplicationPermissionsSoD
            sod1 = appmodels.ApplicationPermissionsSoD()
            sod1.permission_sod = sod1_description

            sod2: appmodels.ApplicationPermissionsSoD
            sod2 = appmodels.ApplicationPermissionsSoD()
            sod2.permission_sod = sod2_description

            list_model_sods = [
                sod1,
                sod2,
            ]
            appmodels.ApplicationPermissionsSoD.objects.bulk_create(
                list_model_sods,
            )

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully included")
            % {
                "field": "sod",
            },
        )

        return redirect(
            "app:application:permissions:sod:page",
        )

    except ValueError as e:
        if str(e) in (
            "form_is_not_valid",
            "sod_already_exists",
        ):
            request.session["SOD_SAVE"] = request.POST
            request.session.modified = True

            return redirect(
                "app:application:permissions:sod:page",
            )

        raise ValueError(e)
