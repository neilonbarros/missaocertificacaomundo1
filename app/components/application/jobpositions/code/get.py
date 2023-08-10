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
    codejobposition: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    elif codejobposition == "new" and type_page == "view":
        return redirect(
            "app:application:jobpositions:code:edit",
            codejobposition=codejobposition,
        )

    try:
        model_jobpositions: appmodels.ApplicationJobPositions
        model_jobpositions = appmodels.ApplicationJobPositions()

        title: str = _("new")

        new_jobposition = request.session.get("JOBPOSITIONSNEW", None)
        if new_jobposition is not None:
            del request.session["JOBPOSITIONSNEW"]

        jobposition_save = request.session.get("JOBPOSITIONSSAVE", None)
        if jobposition_save is not None:
            del request.session["JOBPOSITIONSSAVE"]

        if codejobposition != "new":
            try:
                model_jobpositions = (
                    appmodels.ApplicationJobPositions.objects.get(  # noqa: E501
                        id=codejobposition,
                    )
                )

                title = f"{model_jobpositions.department.department} | {model_jobpositions.jobposition}"  # noqa

            except appmodels.ApplicationJobPositions.DoesNotExist:
                djangomessages.error(
                    request=request,
                    message=_("%(field)s not found")
                    % {
                        "field": _("job position"),
                    },
                )
                raise ValueError("jobpositions_not_found")

        model_departments = appmodels.ApplicationDepartments.objects.all()  # noqa: E501

        form_jobposition: appforms.ApplicationJobPositions
        form_jobposition = appforms.ApplicationJobPositions(
            data=jobposition_save,
            instance=model_jobpositions,
        )
        form_jobposition.is_valid()

        return render(
            request=request,
            template_name="app/application/jobpositions/code/_page.html",  # noqa
            context={
                "settings_debug": settings.DEBUG,
                "sessionuser": session_user,
                "html_language": translation.get_language(),
                "title": title,
                "menu": True,
                "display_center": False,
                "options": "app/application/jobpositions/code/options/_page.html",  # noqa
                "codejobposition": codejobposition,
                "type_page": type_page,
                "new_jobposition": new_jobposition,
                "form_jobposition": form_jobposition,
                "model_departments": model_departments,
            },
        )

    except ValueError as e:
        if str(e) in ("jobpositions_not_found",):
            return redirect(
                "app:application:jobpositions:page",
            )

        raise ValueError(e)
