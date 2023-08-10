import os

from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import components as appcomponents
from app import decorators as appdecorators
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
    codejobposition: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    elif codejobposition == "new":
        return redirect(
            f"{app_name}:application:permissions:page",
        )

    breadcrumbs: list[str] = [
        app_name,
        _(nivel1),
        _(nivel2),
    ]

    try:
        if codejobposition == "new":
            redirect(f"{app_name}:application:permissions:page")

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

            if type_page == "edit":
                breadcrumbs.append(_(type_page))

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

        permissions = []

        permissions += [
            {
                "types": ["view", "edit"],
                "nivel1": {
                    "name": "application",
                    "nivel2": {
                        "name": "departments",
                        "nivel3": {
                            "name": "code",
                            "nivel4": {
                                "name": "",
                                "nivel5": {
                                    "name": "",
                                    "nivel6": {
                                        "name": "",
                                    },
                                },
                            },
                        },
                    },
                },
            },
            {
                "types": ["edit"],
                "nivel1": {
                    "name": "application",
                    "nivel2": {
                        "name": "departments",
                        "nivel3": {
                            "name": "code",
                            "nivel4": {
                                "name": "remove",
                                "nivel5": {
                                    "name": "",
                                    "nivel6": {
                                        "name": "",
                                    },
                                },
                            },
                        },
                    },
                },
            },
            {
                "types": ["view", "edit"],
                "nivel1": {
                    "name": "application",
                    "nivel2": {
                        "name": "jobpositions",
                        "nivel3": {
                            "name": "code",
                            "nivel4": {
                                "name": "",
                                "nivel5": {
                                    "name": "",
                                    "nivel6": {
                                        "name": "",
                                    },
                                },
                            },
                        },
                    },
                },
            },
            {
                "types": ["edit"],
                "nivel1": {
                    "name": "application",
                    "nivel2": {
                        "name": "jobpositions",
                        "nivel3": {
                            "name": "code",
                            "nivel4": {
                                "name": "remove",
                                "nivel5": {
                                    "name": "",
                                    "nivel6": {
                                        "name": "",
                                    },
                                },
                            },
                        },
                    },
                },
            },
            {
                "types": ["view", "edit"],
                "nivel1": {
                    "name": "application",
                    "nivel2": {
                        "name": "permissions",
                        "nivel3": {
                            "name": "code",
                            "nivel4": {
                                "name": "",
                                "nivel5": {
                                    "name": "",
                                    "nivel6": {
                                        "name": "",
                                    },
                                },
                            },
                        },
                    },
                },
            },
            {
                "types": ["view", "edit"],
                "nivel1": {
                    "name": "application",
                    "nivel2": {
                        "name": "peoples",
                        "nivel3": {
                            "name": "code",
                            "nivel4": {
                                "name": "",
                                "nivel5": {
                                    "name": "",
                                    "nivel6": {
                                        "name": "",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        ]

        return render(
            request=request,
            template_name="app/application/permissions/code/_page.html",  # noqa
            context={
                "settings_debug": settings.DEBUG,
                "sessionuser": session_user,
                "app_name": app_name,
                "html_language": translation.get_language(),
                "title": title,
                "menu": True,
                "display_center": False,
                "breadcrumbs": breadcrumbs,
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
                f"{app_name}:application:permissions:page",
            )

        raise ValueError(e)
