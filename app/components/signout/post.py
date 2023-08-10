from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect

app_name: str = "app"


def signout(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    if request.session.get("user", None) is not None:
        del request.session["user"]

    return redirect("app:signin:page")
