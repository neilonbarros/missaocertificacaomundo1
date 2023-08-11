from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from rich import print

from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.not_authenticated()
def signup(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        raise Http404()

    signup_form: appforms.SignUp = appforms.SignUp(
        request.POST,
    )

    cpf: str = ""
    try:
        if signup_form.is_valid() is False:
            print(signup_form.errors.as_json())
            # djangomessages.error(
            #     request=request,
            #     message=_("there are fields to check"),
            # )
            raise ValueError("form_is_invalid")

        signup_cleaned = signup_form.clean()
        cpf = str(signup_cleaned.get("cpf"))
        password_provisional = str(signup_cleaned.get("password_provisional"))
        password = str(signup_cleaned.get("password"))

        model_peoples: appmodels.ApplicationPeoples
        try:
            model_peoples = appmodels.ApplicationPeoples.objects.get(
                cpf=cpf,
                status=True,
            )

        except appmodels.ApplicationPeoples.DoesNotExist:
            raise ValueError("cpf_password_invalid")

        model_passwords: appmodels.ApplicationPasswords
        try:
            model_passwords = appmodels.ApplicationPasswords.objects.get(
                people=model_peoples,
            )

        except appmodels.ApplicationPasswords.DoesNotExist:
            raise ValueError("cpf_password_invalid")

        if (
            apppackages.text.hashed.is_correct_password(
                salt=model_passwords.salt,
                pw_hash=model_passwords.hashed,
                password=password_provisional,
            )
            is False
        ):
            raise ValueError("cpf_password_invalid")

        else:
            model_passwords = appmodels.ApplicationPasswords()
            salt, hashed = apppackages.text.hashed.hash_new_password(password)  # type: ignore # noqa

            try:
                model_passwords = appmodels.ApplicationPasswords.objects.get(
                    people=model_peoples,
                )

                model_passwords.provisional = False
                model_passwords.salt = salt
                model_passwords.hashed = hashed

            except appmodels.ApplicationPasswords.DoesNotExist:
                model_passwords.provisional = False
                model_passwords.salt = salt
                model_passwords.hashed = hashed
                model_passwords.people = model_peoples

            model_passwords.save()

        request.session["SIGNIN_CPF"] = cpf
        request.session.modified = True
        return redirect("app:signin:page")

    except ValueError as e:
        if str(e) in (
            "form_is_invalid",
            "cpf_password_invalid",
        ):
            request.session["SIGNUP_POST"] = request.POST
            request.session.modified = True

            if str(e) in ("cpf_password_invalid",):
                message = f"{_('cpf')}/{_('password')} {('invalid')}"
                djangomessages.error(
                    request=request,
                    message=message,
                )
            return redirect("app:signup:page")

        raise ValueError(e)
