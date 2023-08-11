from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import components as appcomponents
from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
def page(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    model_peoples = appmodels.ApplicationPeoples()

    try:
        model_peoples = appmodels.ApplicationPeoples.objects.select_related(
            "jobposition",
            "department",
        ).get(
            id=session_user.user.id,
            status=True,
        )

    except appmodels.ApplicationPeoples.DoesNotExist:
        return appcomponents.signout.post.signout(request, True)

    password_save = request.session.get("PASSWORD_SAVE", None)
    if password_save is not None:
        del request.session["PASSWORD_SAVE"]

    form_password = appforms.ConfigurationPassword(
        data=password_save
    )

    title: str = _("configuration")

    return render(
        request=request,
        template_name="app/application/configuration/_page.html",  # noqa
        context={
            "settings_debug": settings.DEBUG,
            "sessionuser": session_user,
            "html_language": translation.get_language(),
            "title": title,
            "menu": True,
            "display_center": False,
            "model_peoples": model_peoples,
            "form_password": form_password,
        },
    )
