from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

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
    codedepartment: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    elif codedepartment == "new" and type_page == "view":
        return redirect(
            "app:application:departments:code:edit",
            codedepartment=codedepartment,
        )

    try:
        model_departments: appmodels.ApplicationDepartments
        model_departments = appmodels.ApplicationDepartments()

        title: str = _("new")

        new_department = request.session.get("DEPARTMENTSNEW", None)
        if new_department is not None:
            del request.session["DEPARTMENTSNEW"]

        department_save = request.session.get("DEPARTMENTSAVE", None)
        if department_save is not None:
            del request.session["DEPARTMENTSAVE"]

        if codedepartment != "new":
            try:
                model_departments = (
                    appmodels.ApplicationDepartments.objects.get(  # noqa: E501
                        id=codedepartment,
                    )
                )
                title = model_departments.department

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
            data=department_save,
            instance=model_departments,
        )
        form_department.is_valid()

        return render(
            request=request,
            template_name="app/application/departments/code/_page.html",  # noqa
            context={
                "settings_debug": settings.DEBUG,
                "sessionuser": session_user,
                "html_language": translation.get_language(),
                "title": title,
                "menu": True,
                "display_center": False,
                "options": "app/application/departments/code/options/_page.html",  # noqa
                "codedepartment": codedepartment,
                "type_page": type_page,
                "new_department": new_department,
                "form_department": form_department,
            },
        )

    except ValueError as e:
        if str(e) in ("department_not_found",):
            return redirect(
                "app:application:departments:page",
            )

        raise ValueError(e)
