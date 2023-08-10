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

    elif codedepartment == "new":
        return redirect(
            "app:application:departments:code:edit",
            codedepartment=codedepartment,
        )

    try:
        try:
            result: appmodels.ApplicationDepartments
            result = appmodels.ApplicationDepartments.objects.get(  # noqa: E501
                id=codedepartment,
            )

            title: str = result.department

        except appmodels.ApplicationDepartments.DoesNotExist:
            djangomessages.error(
                request=request,
                message=_("%(field)s not found")
                % {
                    "field": _("department"),
                },
            )
            raise ValueError("department_not_found")

        return render(
            request=request,
            template_name="app/application/departments/code/remove/_page.html",  # noqa
            context={
                "settings_debug": settings.DEBUG,
                "sessionuser": session_user,
                "html_language": translation.get_language(),
                "title": title,
                "menu": False,
                "display_center": True,
                "codedepartment": codedepartment,
                "type_page": type_page,
            },
        )

    except ValueError as e:
        if str(e) in ("department_not_found",):
            return redirect(
                "app:application:departments:page",
            )

        raise ValueError(e)
