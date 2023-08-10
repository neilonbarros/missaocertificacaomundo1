from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=__file__,
)
def remove(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codedepartment: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    if codedepartment == "new":
        return redirect(
            "app:application:departments:page",
            codedepartment=codedepartment,
            type="edit",
        )

    try:
        try:
            model_departments: appmodels.ApplicationDepartments
            model_departments = (
                appmodels.ApplicationDepartments.objects.get(  # noqa: E501
                    id=codedepartment,
                )
            )

            model_departments.delete()

        except appmodels.ApplicationDepartments.DoesNotExist:
            djangomessages.error(
                request=request,
                message=_("%(field)s not found")
                % {
                    "field": _("department"),
                },
            )
            raise ValueError("departments_not_found")

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully removed")
            % {
                "field": _("department"),
            },
        )

        return redirect(
            "app:application:departments:page",
        )

    except ValueError as e:
        if str(e) in ("departments_not_found",):
            return redirect(
                "app:application:departments:page",
            )

        raise ValueError(e)
