from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import forms as appforms
from app import packages as apppackages


@appdecorators.authenticated.not_authenticated()
def page(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    signup_form: appforms.SigIn = appforms.SigIn()

    signup_cpf: str = request.session.get("SIGNUP_CPF", None)
    pyotp_base32secret: str = request.session.get(
        "SIGNUP_PYOTP_BASE32SECRET",
        None,
    )

    if pyotp_base32secret is None:
        pyotp_base32secret = apppackages.py_otp.generate_secret()

        request.session["SIGNUP_PYOTP_BASE32SECRET"] = pyotp_base32secret

    print(Path(__file__))
    branch: str = str(
        Path(__file__).resolve().parent.parent.parent.parent.parent
    ).split("/")[
        -1
    ]  # noqa: E501
    pyotp_uri: str = apppackages.py_otp.generate_uri(
        base32secret=pyotp_base32secret,
        app_name=branch,
    )

    title: str = _("get token")

    return render(
        request=request,
        template_name="app/signup/_page.html",
        context={
            "settings_debug": settings.DEBUG,
            "html_language": translation.get_language(),
            "title": title,
            "menu": False,
            "display_center": False,
            "pyotp_uri": pyotp_uri,
            "pyotp_base32secret": pyotp_base32secret,
            "signup_form": signup_form,
            "signup_cpf": signup_cpf,
        },
    )
