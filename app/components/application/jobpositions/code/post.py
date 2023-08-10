from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=__file__,
)
def save(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codejobposition: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    try:
        model_jobpositions: appmodels.ApplicationJobPositions
        model_jobpositions = appmodels.ApplicationJobPositions()

        if codejobposition == "new":
            request.session.update({"JOBPOSITIONSNEW": "true"})

        else:
            try:
                model_jobpositions = (
                    appmodels.ApplicationJobPositions.objects.get(  # noqa: E501
                        id=codejobposition,
                    )
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

        form_jobposition: appforms.ApplicationJobPositions
        form_jobposition = appforms.ApplicationJobPositions(
            data=request.POST,
            instance=model_jobpositions,
        )

        if form_jobposition.is_valid() is False:
            print(form_jobposition.errors.as_json())
            djangomessages.error(
                request=request,
                message=_("there are fields to check"),
            )
            if "__all__" in list(form_jobposition.errors.as_data().keys()):
                for err in form_jobposition.errors.as_data()["__all__"][0]:
                    djangomessages.error(
                        request=request,
                        message=err.replace("regjobpos", ""),  # type: ignore
                    )
            raise ValueError("form_is_not_valid")

        form_jobposition.save()

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully saved")
            % {
                "field": _("job position"),
            },
        )

        return redirect(
            "app:application:jobpositions:code:view",
            codejobposition=form_jobposition.instance.id,
        )

    except ValueError as e:
        if str(e) in ("form_is_not_valid",):
            request.session["JOBPOSITIONSSAVE"] = request.POST
            request.session.modified = True
            return redirect(
                "app:application:jobpositions:code:edit",
                codejobposition=codejobposition,
            )

        elif str(e) in ("jobpositions_already_exists",):
            return redirect(
                "app:application:jobpositions:code:edit",
                codejobposition=codejobposition,
            )

        elif str(e) in ("jobpositions_not_found",):
            return redirect(
                "app:application:jobpositions:page",
            )

        raise ValueError(e)
