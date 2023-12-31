from django.conf import settings
from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import forms as appforms
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=__file__,
)
def page(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codepeople: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "GET":
        raise Http404()

    elif codepeople == "new" and type_page == "view":
        return redirect(
            "app:application:peoples:code:edit",
            codepeople=codepeople,
        )

    try:
        model_peoples: appmodels.ApplicationPeoples
        model_peoples = appmodels.ApplicationPeoples()

        title: str = _("new")

        new_people = request.session.get("PEOPLESNEW", None)
        if new_people is not None:
            del request.session["PEOPLESNEW"]

        people_save = request.session.get("PEOPLESSAVE", None)
        if people_save is not None:
            del request.session["PEOPLESSAVE"]

        if codepeople != "new":
            try:
                model_peoples = appmodels.ApplicationPeoples.objects.get(  # noqa: E501
                    id=codepeople,
                )
                title = model_peoples.fullname

            except appmodels.ApplicationPeoples.DoesNotExist:
                djangomessages.error(
                    request=request,
                    message=_("%(field)s not found")
                    % {
                        "field": _("people"),
                    },
                )
                raise ValueError("peoples_not_found")

        model_jobpositions = (
            appmodels.ApplicationJobPositions.objects.all()
            .order_by("jobposition")  # noqa: E501
            .select_related(
                "department",
            )
        )

        model_passwords = appmodels.ApplicationPasswords()

        try:
            model_passwords = appmodels.ApplicationPasswords.objects.get(
                people=model_peoples,
            )

        except appmodels.ApplicationPasswords.DoesNotExist:
            ...

        form_people: appforms.ApplicationPeoples
        form_people = appforms.ApplicationPeoples(
            data=people_save,
            instance=model_peoples,
        )
        form_people.is_valid()

        return render(
            request=request,
            template_name="app/application/peoples/code/_page.html",  # noqa
            context={
                "settings_debug": settings.DEBUG,
                "sessionuser": session_user,
                "html_language": translation.get_language(),
                "title": title,
                "menu": True,
                "display_center": False,
                "options": "app/application/peoples/code/options/_page.html",  # noqa
                "codepeople": codepeople,
                "type_page": type_page,
                "new_people": new_people,
                "model_jobpositions": model_jobpositions,
                "form_people": form_people,
                "provisional": model_passwords.provisional,
                "provisional_code": apppackages.utils.id_generator(
                    size=10,
                    letter=True,
                    digits=True,
                ),
            },
        )

    except ValueError as e:
        if str(e) in ("peoples_not_found",):
            return redirect(
                "app:application:peoples:page",
            )

        raise ValueError(e)
