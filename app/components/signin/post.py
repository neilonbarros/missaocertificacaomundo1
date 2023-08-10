from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone as djangotimezone
from django.utils.translation import gettext_lazy as _
from rich import print

from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.not_authenticated()
def signin(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        raise Http404()

    signin_form: appforms.SigIn = appforms.SigIn(
        request.POST,
    )

    cpf: str = ""
    try:
        if signin_form.is_valid() is False:
            print(signin_form.errors.as_json())
            # djangomessages.error(
            #     request=request,
            #     message=_("there are fields to check"),
            # )
            raise ValueError("form_is_invalid")

        signin_cleaned = signin_form.clean()
        cpf = str(signin_cleaned.get("cpf"))
        password = str(signin_cleaned.get("password"))

        people_model: appmodels.ApplicationPeoples
        try:
            people_model = appmodels.ApplicationPeoples.objects.get(
                cpf=cpf,
                status=True,
            )

        except appmodels.ApplicationPeoples.DoesNotExist:
            raise ValueError("cpf_password_invalid")

        password_model: appmodels.ApplicationPasswords
        try:
            password_model = appmodels.ApplicationPasswords.objects.get(
                people=people_model,
            )

        except appmodels.ApplicationPasswords.DoesNotExist:
            raise ValueError("cpf_password_invalid")

        if (
            apppackages.text.hashed.is_correct_password(
                salt=password_model.salt,
                pw_hash=password_model.hashed,
                password=password,
            )
            is False
        ):
            raise ValueError("cpf_password_invalid")

        session_user: apppackages.utils.Session
        session_user = apppackages.utils.Session(request=request)
        session_user.lifetime = djangotimezone.now().date()
        session_user.user.id = people_model.id
        session_user.user.fullname = people_model.fullname

        request.session.update(session_user.save())
        request.session.modified = True

        if settings.DEBUG is True:
            print(__file__)
            print(request.session.__dict__)

        return redirect("app:home:page")

    except ValueError as e:
        if str(e) in (
            "form_is_invalid",
            "cpf_password_invalid",
        ):
            request.session["SIGNIN_POST"] = request.POST
            request.session.modified = True

            if str(e) in ("cpf_password_invalid",):
                message = _("cpf/password invalid")
                djangomessages.error(
                    request=request,
                    message=message,
                )
            return redirect("app:signin:page")

        raise ValueError(e)
