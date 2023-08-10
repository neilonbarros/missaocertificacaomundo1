from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.not_authenticated()
def signup(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        raise Http404()

    signup_form: appforms.SigIn = appforms.SigIn(
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
            raise ValueError("cpf_token_invalid")

        signup_cleaned = signup_form.clean()
        cpf = str(signup_cleaned.get("cpf"))
        token = str(signup_cleaned.get("token"))

        request.session["SIGNUP_CPF"] = cpf

        users_model: appmodels.ApplicationUsers
        try:
            users_model = appmodels.ApplicationUsers.objects.get(
                cpf_user=cpf,
            )

        except appmodels.ApplicationUsers.DoesNotExist:
            raise ValueError("cpf_token_invalid")

        if appmodels.ApplicationAuths.objects.filter(
            users_auth_id=users_model.id_user,
        ).exists():
            raise ValueError("user_has_access")

        base32secret = request.session["SIGNUP_PYOTP_BASE32SECRET"]
        if (
            apppackages.py_otp.validate(
                base32secret=base32secret,
                token=token,
            )
            is False
        ):
            raise ValueError("cpf_token_invalid")

        auths_model: appmodels.ApplicationAuths = appmodels.ApplicationAuths()
        auths_model.users_auth = users_model
        auths_model.auth_auth = base32secret
        auths_model.save()

        request.session["SIGNIN_CPF"] = cpf

        del request.session["SIGNUP_CPF"]
        del request.session["SIGNUP_PYOTP_BASE32SECRET"]

        djangomessages.success(
            request=request,
            message=_("access created"),
        )
        return redirect("app:signin:page")

    except ValueError as e:
        if str(e) == "cpf_token_invalid":
            message = _("cpf/token invalid")
            djangomessages.error(
                request=request,
                message=message,
            )
            return redirect("app:signup:page")

        elif str(e) == "user_has_access":
            message = _("user already has access")
            djangomessages.info(
                request=request,
                message=message,
            )
            return redirect("app:signin:page")

        raise ValueError(e)
