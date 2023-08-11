from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _

from app import decorators as appdecorators
from app import forms as appforms


@appdecorators.authenticated.not_authenticated()
def page(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    signin_post = {}
    signin_form: appforms.SignIn = appforms.SignIn()

    if request.session.get("SIGNIN_POST", None) is not None:
        signin_post = request.session["SIGNIN_POST"]
        del request.session["SIGNIN_POST"]

        signin_form = appforms.SignIn(data=signin_post)
        signin_form.is_valid()

    elif request.session.get("SIGNIN_CPF", None) is not None:
        signin_post = {"cpf": request.session.get("SIGNIN_CPF", None)}
        del request.session["SIGNIN_CPF"]

    signin_cpf = signin_post.get(
        "cpf",
        None,
    )

    title: str = _("sign in")

    return render(
        request=request,
        template_name="app/signin/_page.html",
        context={
            "settings_debug": settings.DEBUG,
            "html_language": translation.get_language(),
            "title": title,
            "menu": False,
            "display_center": True,
            "signin_form": signin_form,
            "signin_cpf": signin_cpf,
        },
    )
