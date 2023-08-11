from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from rich import print

from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=__file__,
)
def save(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codepeople: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    try:
        model_peoples: appmodels.ApplicationPeoples
        model_peoples = appmodels.ApplicationPeoples()

        if codepeople == "new":
            request.session.update({"PEOPLESNEW": "true"})

        else:
            try:
                model_peoples = appmodels.ApplicationPeoples.objects.get(
                    id=codepeople,
                )

            except appmodels.ApplicationPeoples.DoesNotExist:
                djangomessages.error(
                    request=request,
                    message=_("%(field)s not found")
                    % {
                        "field": _("people"),
                    },
                )
                raise ValueError("peoples_not_found")

        form_people: appforms.ApplicationPeoples
        form_people = appforms.ApplicationPeoples(
            data=request.POST,
            instance=model_peoples,
        )

        if form_people.is_valid() is False:
            print(form_people.errors.as_json())
            djangomessages.error(
                request=request,
                message=_("there are fields to check"),
            )
            if "__all__" in list(form_people.errors.as_data().keys()):
                for err in form_people.errors.as_data()["__all__"][0]:
                    djangomessages.error(
                        request=request,
                        message=err.replace("apppeo", ""),  # type: ignore
                    )
            raise ValueError("form_is_not_valid")

        provisional = request.POST.get("selectProvisionalName", None)
        provisional_code = request.POST.get("inputProvisionalCodeName", None)

        if settings.DEBUG is True:
            print(__file__)
            print(provisional)
            print(provisional_code)

        if provisional is not None and provisional == "True":
            model_passwords = appmodels.ApplicationPasswords()
            salt, hashed = apppackages.text.hashed.hash_new_password(provisional_code)  # type: ignore # noqa

            try:
                model_passwords = appmodels.ApplicationPasswords.objects.get(
                    people=model_peoples,
                )

                model_passwords.provisional = True
                model_passwords.salt = salt
                model_passwords.hashed = hashed

            except appmodels.ApplicationPasswords.DoesNotExist:
                model_passwords.provisional = True
                model_passwords.salt = salt
                model_passwords.hashed = hashed
                model_passwords.people = model_peoples

            model_passwords.save()

        form_people.save()

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully saved")
            % {
                "field": _("people"),
            },
        )

        return redirect(
            "app:application:peoples:code:view",
            codepeople=form_people.instance.id,
        )

    except ValueError as e:
        if str(e) in ("form_is_not_valid",):
            request.session["PEOPLESSAVE"] = request.POST
            request.session.modified = True
            return redirect(
                "app:application:peoples:code:edit",
                codepeople=codepeople,
            )

        elif str(e) in ("people_already_exists",):
            return redirect(
                "app:application:peoples:code:edit",
                codepeople=codepeople,
            )

        elif str(e) in ("peoples_not_found",):
            return redirect(
                "app:application:peoples:page",
            )

        raise ValueError(e)
