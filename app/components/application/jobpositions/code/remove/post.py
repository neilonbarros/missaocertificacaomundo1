import os

from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=os.path.dirname(__file__),
)
def remove(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codejobposition: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    if codejobposition == "new":
        return redirect(
            "app:application:jobpositions:page",
            codejobposition=codejobposition,
            type="edit",
        )

    try:
        try:
            model_jobpositions: appmodels.ApplicationJobPositions
            model_jobpositions = (
                appmodels.ApplicationJobPositions.objects.get(  # noqa: E501
                    id=codejobposition,
                )
            )
            model_jobpositions.delete()

        except appmodels.ApplicationJobPositions.DoesNotExist:
            djangomessages.error(
                request=request,
                message=_("%(field)s not found")
                % {
                    "field": _("job position"),
                },
            )
            raise ValueError("jobpositions_not_found")

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully removed")
            % {
                "field": _("job position"),
            },
        )

        return redirect(
            "app:application:jobpositions:page",
        )

    except ValueError as e:
        if str(e) in ("jobpositions_not_found",):
            return redirect(
                "app:application:jobpositions:page",
            )

        raise ValueError(e)
