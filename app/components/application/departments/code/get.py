import os

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

app_name: str = "app"


subdirs: list = os.path.dirname(__file__).split("/")
nivel1: str = subdirs[-3]
nivel2: str = subdirs[-2]


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    app_name=app_name,
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
            f"{app_name}:application:departments:code:edit",
            codedepartment=codedepartment,
        )

    breadcrumbs: list[str] = [
        app_name,
        _(nivel1),
        _(nivel2),
    ]

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

                if type_page == "edit":
                    breadcrumbs.append(_(type_page))

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
                "app_name": app_name,
                "html_language": translation.get_language(),
                "title": title,
                "menu": True,
                "display_center": False,
                "breadcrumbs": breadcrumbs,
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
                f"{app_name}:application:departments:page",
            )

        raise ValueError(e)
