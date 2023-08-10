from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect

from app import decorators as appdecorators
from app import packages as apppackages

app_name: str = "app"


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    app_name=app_name,
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
            f"{app_name}:application:jobpositions:page",
        )

    except ValueError as e:
        raise ValueError(e)
