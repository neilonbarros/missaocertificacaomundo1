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

    signup_post = {}
    signup_form: appforms.SignUp = appforms.SignUp()

    if request.session.get("SIGNUP_POST", None) is not None:
        signup_post = request.session["SIGNUP_POST"]
        del request.session["SIGNUP_POST"]

        signup_form = appforms.SignUp(data=signup_post)
        signup_form.is_valid()

    elif request.session.get("SIGNUP_CPF", None) is not None:
        signup_post = {"cpf": request.session.get("SIGNUP_CPF", None)}
        del request.session["SIGNUP_CPF"]

    signup_cpf = signup_post.get(
        "cpf",
        None,
    )

    title: str = _("sign in")

    return render(
        request=request,
        template_name="app/signup/_page.html",
        context={
            "settings_debug": settings.DEBUG,
            "html_language": translation.get_language(),
            "title": title,
            "menu": False,
            "display_center": True,
            "signup_form": signup_form,
            "signup_cpf": signup_cpf,
        },
    )
