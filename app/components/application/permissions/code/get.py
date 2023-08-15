from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import models as appmodels
from app import packages as apppackages

permissions = []

permissions += [
    {
        "types": ["view"],
        "nivel1": "menu1",
        "nivel2": "submenu1",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view"],
        "nivel1": "menu1",
        "nivel2": "submenu2",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view"],
        "nivel1": "menu1",
        "nivel2": "submenu3",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
]

permissions += [
    {
        "types": ["view"],
        "nivel1": "menu2",
        "nivel2": "submenu1",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view"],
        "nivel1": "menu2",
        "nivel2": "submenu2",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view"],
        "nivel1": "menu2",
        "nivel2": "submenu3",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
]

permissions += [
    {
        "types": ["view"],
        "nivel1": "menu3",
        "nivel2": "submenu1",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view"],
        "nivel1": "menu3",
        "nivel2": "submenu2",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view"],
        "nivel1": "menu3",
        "nivel2": "submenu3",
        "nivel3": None,
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
]

permissions += [
    {
        "types": ["view", "edit"],
        "nivel1": "application",
        "nivel2": "departments",
        "nivel3": "code",
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view", "edit"],
        "nivel1": "application",
        "nivel2": "jobpositions",
        "nivel3": "code",
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view", "edit"],
        "nivel1": "application",
        "nivel2": "permissions",
        "nivel3": "code",
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view", "edit"],
        "nivel1": "application",
        "nivel2": "permissions",
        "nivel3": "sod",
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
    {
        "types": ["view", "edit"],
        "nivel1": "application",
        "nivel2": "peoples",
        "nivel3": "code",
        "nivel4": None,
        "nivel5": None,
        "nivel6": None,
    },
]


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
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

    elif codejobposition == "new":
        return redirect(
            "app:application:permissions:page",
        )

    try:
        if codejobposition == "new":
            redirect("app:application:permissions:page")

        elif (
            appmodels.ApplicationJobPositions.objects.filter(
                id=codejobposition
            ).exists()
            is False
        ):
            djangomessages.error(
                request=request,
                message=_("%(field)s not found")
                % {
                    "field": _("job position"),
                },
            )
            raise ValueError("jobpositions_not_found")

        model_jobpositions: appmodels.ApplicationJobPositions
        try:
            model_jobpositions = (
                appmodels.ApplicationJobPositions.objects.get(  # noqa: E501
                    id=codejobposition,
                )
            )
            title = model_jobpositions.jobposition

        except appmodels.ApplicationJobPositions.DoesNotExist:
            djangomessages.error(
                request=request,
                message=_("%(field)s not found")
                % {
                    "field": _("job position"),
                },
            )
            raise ValueError("jobpositions_not_found")

        model_permissions = (
            appmodels.ApplicationPermissions.objects.filter(  # noqa: E501
                jobposition=model_jobpositions
            )
        )

        result_permissions: list[str]
        result_permissions = []

        for x in model_permissions:
            result_permissions.append(x.permission)

        return render(
            request=request,
            template_name="app/application/permissions/code/_page.html",  # noqa
            context={
                "settings_debug": settings.DEBUG,
                "sessionuser": session_user,
                "html_language": translation.get_language(),
                "title": title,
                "menu": True,
                "display_center": False,
                "options": "app/application/permissions/code/options/_page.html",  # noqa
                "codejobposition": codejobposition,
                "type_page": type_page,
                "permissions": permissions,
                "result_permissions": result_permissions,
            },
        )

    except ValueError as e:
        if str(e) in ("jobpositions_not_found",):
            return redirect(
                "app:application:permissions:page",
            )

        raise ValueError(e)
