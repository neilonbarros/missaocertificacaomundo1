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
    codedepartment: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    try:
        model_departments: appmodels.ApplicationDepartments
        model_departments = appmodels.ApplicationDepartments()

        if codedepartment == "new":
            request.session.update({"DEPARTMENTSNEW": "true"})

        else:
            try:
                model_departments = (
                    appmodels.ApplicationDepartments.objects.get(  # noqa: E501
                        id=codedepartment,
                    )
                )

            except appmodels.ApplicationDepartments.DoesNotExist:
                djangomessages.error(
                    request=request,
                    message=_("%(field)s not found")
                    % {
                        "field": _("department"),
                    },
                )
                raise ValueError("department_not_found")

        form_department: appforms.ApplicationDepartment
        form_department = appforms.ApplicationDepartment(
            data=request.POST,
            instance=model_departments,
        )

        if form_department.is_valid() is False:
            print(form_department.errors.as_json())
            djangomessages.error(
                request=request,
                message=_("there are fields to check"),
            )
            raise ValueError("form_is_not_valid")

        form_department.save()

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully saved")
            % {
                "field": _("department"),
            },
        )

        return redirect(
            "app:application:departments:code:view",
            codedepartment=form_department.instance.id,
        )

    except ValueError as e:
        if str(e) in ("form_is_not_valid",):
            request.session["DEPARTMENTSAVE"] = request.POST
            request.session.modified = True
            return redirect(
                "app:application:departments:code:edit",
                codedepartment=codedepartment,
            )

        elif str(e) in ("department_already_exists",):
            return redirect(
                "app:application:departments:code:edit",
                codedepartment=codedepartment,
            )

        elif str(e) in ("department_not_found",):
            return redirect(
                "app:application:departments:page",
            )

        raise ValueError(e)
