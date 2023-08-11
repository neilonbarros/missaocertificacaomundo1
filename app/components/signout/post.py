from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect


def signout(request: HttpRequest, without_post: bool = False) -> HttpResponse:
    if request.method != "POST" and without_post is False:
        raise Http404()

    if request.session.get("user", None) is not None:
        del request.session["user"]

    return redirect("app:signin:page")
