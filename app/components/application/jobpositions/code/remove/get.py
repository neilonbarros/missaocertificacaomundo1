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

app_name: str = "app"

subdirs: list = os.path.dirname(__file__).split("/")
nivel1: str = subdirs[-4]
nivel2: str = subdirs[-3]


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    app_name=app_name,
    file=__file__,
)
def page(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codejobposition: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    elif codejobposition == 0:
        return redirect(
            f"{app_name}:application:jobpositions:page",
            codejobposition=codejobposition,
            type="edit",
        )

    breadcrumbs: list[str] = [
        app_name,
        _(nivel1),
        _(nivel2),
        _("remove"),
    ]

    try:
        try:
            result: appmodels.ApplicationJobPositions
            result = appmodels.ApplicationJobPositions.objects.get(  # noqa: E501
                id=codejobposition,
            )

            title: str = (
                f"{result.department.department} | {result.jobposition}"  # noqa
            )

        except appmodels.ApplicationJobPositions.DoesNotExist:
            djangomessages.error(
                request=request,
                message=_("%(field)s not found")
                % {
                    "field": _("job position"),
                },
            )
            raise ValueError("jobpositions_not_found")

        return render(
            request=request,
            template_name="app/application/jobpositions/code/remove/_page.html",  # noqa
            context={
                "settings_debug": settings.DEBUG,
                "sessionuser": session_user,
                "app_name": app_name,
                "html_language": translation.get_language(),
                "title": title,
                "menu": False,
                "display_center": True,
                "breadcrumbs": breadcrumbs,
                "codejobposition": codejobposition,
                "type_page": type_page,
            },
        )

    except ValueError as e:
        if str(e) in ("jobpositions_not_found",):
            return redirect(
                f"{app_name}:application:jobpositions:page",
            )

        raise ValueError(e)
