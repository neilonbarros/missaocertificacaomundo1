from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages

app_name: str = "app"


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    app_name=app_name,
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

        model_appusers: appmodels.ApplicationUsers
        apps: list = []

        model_jobposition: appmodels.ApplicationJobPositions
        model_jobposition = form_people.cleaned_data["jobposition"]  # noqa: E501

        model_jobposition = appmodels.ApplicationJobPositions.objects.get(  # noqa: E501
            id=model_jobposition.id,
        )
        model_peoples.department = model_jobposition.department  # noqa: E501

        status: str = form_people.cleaned_data["status"]
        cpf: str = form_people.cleaned_data["cpf"]

        try:
            model_appusers = appmodels.ApplicationUsers.objects.get(
                id_user=model_peoples.user,
            )

            if model_appusers.apps is not None and model_appusers.apps != "":
                apps = model_appusers.apps.split(",")

            if status is None:
                if app_name in apps:
                    apps.remove(app_name)
                    model_appusers.apps = ",".join(apps)
                    model_appusers.save()

            else:
                if app_name not in apps:
                    apps.append(app_name)
                    model_appusers.apps = ",".join(apps)
                    model_appusers.save()

        except appmodels.ApplicationUsers.DoesNotExist:
            if appmodels.ApplicationUsers.objects.filter(
                cpf_user=cpf,
            ).exists():
                model_appusers = appmodels.ApplicationUsers.objects.get(
                    cpf_user=cpf,
                )

                apps = []
                if (
                    model_appusers.apps is not None
                    and model_appusers.apps != ""  # noqa: E501
                ):  # noqa: E501
                    apps = model_appusers.apps.split(",")

                if status is True and app_name not in apps:
                    apps.append(app_name)
                    model_appusers.apps = ",".join(apps)

            else:
                model_appusers = appmodels.ApplicationUsers()
                model_appusers.cpf_user = cpf

                if status is True:
                    model_appusers.apps = app_name

            model_appusers.save()

        model_peoples.user = model_appusers.id_user

        form_people.save()

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully saved")
            % {
                "field": _("people"),
            },
        )

        return redirect(
            f"{app_name}:application:peoples:code:view",
            codepeople=form_people.instance.id,
        )

    except ValueError as e:
        if str(e) in ("form_is_not_valid",):
            request.session["PEOPLESSAVE"] = request.POST
            request.session.modified = True
            return redirect(
                f"{app_name}:application:peoples:code:edit",
                codepeople=codepeople,
            )

        elif str(e) in ("people_already_exists",):
            return redirect(
                f"{app_name}:application:peoples:code:edit",
                codepeople=codepeople,
            )

        elif str(e) in ("peoples_not_found",):
            return redirect(
                f"{app_name}:application:peoples:page",
            )

        raise ValueError(e)
