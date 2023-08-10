from typing import Any, Optional

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
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
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    search_jobpositions_post: bool
    search_jobpositions_post = request.session.get(
        "JOBPOSITIONSSEARCH_POST", False
    )  # noqa: E501

    if search_jobpositions_post is True:
        del request.session["JOBPOSITIONSSEARCH_POST"]

    search_jobpositions: Optional[dict[str, Any]]
    search_jobpositions = request.session.get("JOBPOSITIONSSEARCH", None)

    search_department: Optional[int] = None
    search_jobposition: Optional[str] = None

    if search_jobpositions is not None:
        search_department = search_jobpositions.get(
            "search_department", None
        )  # noqa: E501

        if (
            search_department is not None and search_department == "all"  # noqa: E501
        ):  # noqa: E501
            search_department = None

        search_jobposition = search_jobpositions.get(
            "search_jobposition", None
        )  # noqa: E501

        if search_jobposition in ("", None):
            search_jobposition = None

        else:
            search_jobposition = search_jobposition.lower().strip()  # type: ignore # noqa: E501

    model_departments = (
        appmodels.ApplicationDepartments.objects.all().order_by(  # noqa: E501
            "department"
        )
    )

    if search_jobpositions_post is True:
        overview_jobpositions = appmodels.ApplicationJobPositions.objects.filter(
            id__gt=0
        )  # noqa: E501  # noqa: E501

        if search_department is not None or search_jobposition is not None:
            if search_department is not None:
                overview_jobpositions = (
                    overview_jobpositions
                    & overview_jobpositions.filter(  # noqa: E501
                        department=search_department,
                    )
                )

            if search_jobposition is not None:
                overview_jobpositions = (
                    overview_jobpositions
                    & overview_jobpositions.filter(  # noqa: E501
                        jobposition__contains=search_jobposition,  # noqa: E501
                    )
                )

        else:
            overview_jobpositions = overview_jobpositions.all()

        overview_jobpositions = overview_jobpositions.select_related(
            "department",
        )

    else:
        overview_jobpositions = appmodels.ApplicationJobPositions()

    title: str = _("job positions")

    return render(
        request=request,
        template_name="app/application/jobpositions/_page.html",  # noqa
        context={
            "settings_debug": settings.DEBUG,
            "sessionuser": session_user,
            "html_language": translation.get_language(),
            "title": title,
            "menu": True,
            "display_center": False,
            "options": "app/application/jobpositions/options/_page.html",  # noqa
            "search_jobpositions_post": search_jobpositions_post,
            "search_department": search_department,
            "search_jobposition": search_jobposition,
            "model_departments": model_departments,
            "overview_jobpositions": overview_jobpositions,
        },
    )
