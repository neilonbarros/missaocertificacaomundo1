from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
def page(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    title: str = _("sign out")
    return render(
        request=request,
        template_name="app/signout/_page.html",
        context={
            "settings_debug": settings.DEBUG,
            "sessionuser": session_user,
            "html_language": translation.get_language(),
            "title": title,
            "menu": False,
            "display_center": True,
        },
    )
