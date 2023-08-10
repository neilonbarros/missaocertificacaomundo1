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

    search_peoples_post: bool
    search_peoples_post = request.session.get(
        "SEARCH_PEOPLES_POST", False
    )  # noqa: E501

    if search_peoples_post is True:
        del request.session["SEARCH_PEOPLES_POST"]

    search_peoples: Optional[dict[str, Any]]
    search_peoples = request.session.get("SEARCH_PEOPLES", None)

    search_department: Optional[str] = None
    search_jobposition: Optional[int] = None
    search_people: Optional[str] = None

    if search_peoples is not None:
        search_department = search_peoples.get("search_department", None)  # noqa: E501

        if (
            search_department is not None and search_department == "all"  # noqa: E501
        ):  # noqa: E501
            search_department = None

        search_jobposition = search_peoples.get(
            "search_jobposition", None
        )  # noqa: E501

        if (
            search_jobposition is not None and search_jobposition == "all"  # noqa: E501
        ):  # noqa: E501
            search_jobposition = None

        search_people = search_peoples.get("search_people", None)  # noqa: E501

        if search_people in ("", None):
            search_people = None

        else:
            search_people = search_people.lower().strip()  # type: ignore # noqa: E501

    model_departments = (
        appmodels.ApplicationDepartments.objects.all().order_by(  # noqa: E501
            "department"
        )
    )

    model_jobpositions = (
        appmodels.ApplicationJobPositions.objects.all().order_by(  # noqa: E501
            "jobposition"
        )
    )

    if search_peoples_post is True:
        overview_peoples = appmodels.ApplicationPeoples.objects.filter(  # noqa: E501
            id__gt=0
        )  # noqa: E501

        if (
            search_department is not None
            or search_jobposition is not None
            or search_people is not None
        ):
            if search_department is not None:
                overview_peoples = (
                    overview_peoples
                    & overview_peoples.filter(  # noqa: E501
                        department=search_department,
                    )
                )

            if search_jobposition is not None:
                overview_peoples = (
                    overview_peoples
                    & overview_peoples.filter(  # noqa: E501
                        jobposition=search_jobposition,
                    )
                )

            if search_people is not None:
                overview_peoples = (
                    overview_peoples
                    & overview_peoples.filter(  # noqa: E501
                        fullname__contains=search_people,  # noqa: E501
                    )
                )

        else:
            overview_peoples = overview_peoples.all()

        overview_peoples = overview_peoples.select_related(
            "jobposition",
            "department",
        )

    else:
        overview_peoples = appmodels.ApplicationPeoples()

    title: str = _("peoples")

    return render(
        request=request,
        template_name="app/application/peoples/_page.html",  # noqa
        context={
            "settings_debug": settings.DEBUG,
            "sessionuser": session_user,
            "html_language": translation.get_language(),
            "title": title,
            "menu": True,
            "display_center": False,
            "options": "app/application/peoples/options/_page.html",  # noqa
            "search_peoples_post": search_peoples_post,
            "search_department": search_department,
            "search_jobposition": search_jobposition,
            "search_people": search_people,
            "model_departments": model_departments,
            "model_jobpositions": model_jobpositions,
            "overview_peoples": overview_peoples,
        },
    )
