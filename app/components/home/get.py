from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.load(
    model_permissions=appmodels.ApplicationPermissions,
    model_peoples=appmodels.ApplicationPeoples,
)
def page(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    request.session.update(session_user.save())
    request.session.modified = True

    title: str = _("home")

    return render(
        request=request,
        template_name="app/home/_page.html",
        context={
            "settings_debug": settings.DEBUG,
            "sessionuser": session_user,
            "html_language": translation.get_language(),
            "title": title,
            "menu": True,
            "display_center": False,
        },
    )
