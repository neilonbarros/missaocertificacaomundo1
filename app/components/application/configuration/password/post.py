from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from rich import print

from app import components as appcomponents
from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
def save(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    if settings.DEBUG is True:
        print(__file__)
        print(session_user.user.__dict__)

    try:
        model_peoples = appmodels.ApplicationPeoples()

        try:
            model_peoples = appmodels.ApplicationPeoples.objects.get(
                id=session_user.user.id,
                status=True,
            )

        except appmodels.ApplicationPeoples.DoesNotExist:
            raise ValueError("people_not_exists")

        model_passwords = appmodels.ApplicationPasswords()

        try:
            model_passwords = appmodels.ApplicationPasswords.objects.get(
                people=model_peoples,
            )

        except appmodels.ApplicationPeoples.DoesNotExist:
            raise ValueError("password_not_exists")

        form_conf_password: appforms.ConfigurationPassword
        form_conf_password = appforms.ConfigurationPassword(
            data=request.POST,
        )

        if form_conf_password.is_valid() is False:
            print(form_conf_password.errors.as_json())
            djangomessages.error(
                request=request,
                message=_("there are fields to check"),
            )
            raise ValueError("form_is_not_valid")

        form_cleaned = form_conf_password.cleaned_data
        password = form_cleaned.get("password", None)
        password_new = form_cleaned.get("password_new", None)
        password_new_again = form_cleaned.get("password_new_again", None)

        if (
            apppackages.text.hashed.is_correct_password(
                salt=model_passwords.salt,
                pw_hash=model_passwords.hashed,
                password=password,
            )
            is False
        ):
            session_user.user.password_attempts -= 1

            if session_user.user.password_attempts == 0:
                model_passwords.delete()
                raise ValueError("end_password_attempts")

            else:
                request.session.update(session_user.save())
                request.session.modified = True
                raise ValueError("cpf_password_invalid")

        elif password_new != password_new_again:
            raise ValueError("new_password_invalid")

        salt, hashed = apppackages.text.hashed.hash_new_password(password_new)  # type: ignore # noqa
        model_passwords.salt = salt
        model_passwords.hashed = hashed
        model_passwords.people = model_peoples
        model_passwords.save()

        djangomessages.success(
            request=request,
            message=_("successfully changed %(field)s")
            % {
                "field": _("password"),
            },
        )

        return appcomponents.signout.post.signout(request, True)

    except ValueError as e:
        if str(e) in (
            "form_is_not_valid",
            "cpf_password_invalid",
            "new_password_invalid",
        ):
            if str(e) in ("cpf_password_invalid",):
                message = f"{_('password')} {('invalid')}"
                djangomessages.error(
                    request=request,
                    message=message,
                )

            elif str(e) in ("new_password_invalid",):
                message = _("the new passwords are not the same")
                djangomessages.error(
                    request=request,
                    message=message,
                )

            request.session["PASSWORD_SAVE"] = request.POST
            request.session.modified = True
            return redirect(
                "app:application:configuration:page",
            )

        elif str(e) in (
            "people_not_exists",
            "password_not_exists",
            "end_password_attempts",
        ):
            if str(e) in (
                "people_not_exists",
                "password_not_exists",
            ):
                djangomessages.error(
                    request=request,
                    message=_("without user data"),
                )

            elif str(e) in ("end_password_attempts",):
                message = _("no more attempts")
                djangomessages.error(
                    request=request,
                    message=message,
                )

            return appcomponents.signout.post.signout(request, True)

        raise ValueError(e)
