import os
from typing import Any, Optional

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import models as appmodels
from app import packages as apppackages

app_name: str = "app"

subdirs: list = os.path.dirname(__file__).split("/")
nivel1: str = subdirs[-2]
nivel2: str = subdirs[-1]


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    app_name=app_name,
    file=__file__,
)
def page(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    search_departments_post: bool
    search_departments_post = request.session.get(
        "DEPARTMENTSSEARCH_POST", False
    )  # noqa: E501

    if search_departments_post is True:
        del request.session["DEPARTMENTSSEARCH_POST"]

    search_departments: Optional[dict[str, Any]]
    search_departments = request.session.get("DEPARTMENTSSEARCH", None)

    search_department: Optional[str] = None

    if search_departments is not None:
        search_department = search_departments.get(
            "search_department", None
        )  # noqa: E501

        if search_department in ("", None):
            search_department = None

        else:
            search_department = search_department.lower().strip()  # type: ignore # noqa: E501

    if search_departments_post is True:
        overview_departments = appmodels.ApplicationDepartments.objects.filter(
            id__gt=0
        )  # noqa: E501

        if search_department is not None:  # noqa: E501
            if search_department is not None:
                overview_departments = (
                    overview_departments
                    & overview_departments.filter(  # noqa: E501
                        department__contains=search_department,
                    )
                )

        else:
            overview_departments = overview_departments.all()

    else:
        overview_departments = appmodels.ApplicationDepartments()

    breadcrumbs: list[str] = [
        app_name,
        _(nivel1),
    ]
    title: str = _("departments")

    return render(
        request=request,
        template_name="app/application/departments/_page.html",  # noqa
        context={
            "settings_debug": settings.DEBUG,
            "sessionuser": session_user,
            "app_name": app_name,
            "html_language": translation.get_language(),
            "title": title,
            "menu": True,
            "display_center": False,
            "breadcrumbs": breadcrumbs,
            "options": "app/application/departments/options/_page.html",  # noqa
            "search_departments_post": search_departments_post,
            "search_department": search_department,
            "overview_departments": overview_departments,
        },
    )
