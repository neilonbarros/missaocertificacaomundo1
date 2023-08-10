from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect

from app import decorators as appdecorators
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=__file__,
)
def search(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    try:
        request.session["JOBPOSITIONSSEARCH_POST"] = True
        request.session["JOBPOSITIONSSEARCH"] = request.POST
        request.session.modified = True

        return redirect(
            "app:application:jobpositions:page",
        )

    except ValueError as e:
        raise ValueError(e)
