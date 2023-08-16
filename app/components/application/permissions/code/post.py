from django.contrib import messages as djangomessages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from app import decorators as appdecorators
from app import models as appmodels
from app import packages as apppackages


@appdecorators.authenticated.is_authenticated()
@appdecorators.permissions.validate(
    file=__file__,
)
def save(
    request: HttpRequest,
    session_user: apppackages.utils.Session,
    codejobposition: str,
    type_page: str,
) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    try:
        if codejobposition == "new":
            redirect("app:application:permissions:page")

        elif (
            appmodels.ApplicationJobPositions.objects.filter(
                id=codejobposition
            ).exists()
            is False
        ):
            djangomessages.error(
                request=request,
                message=_("%(field)s not found")
                % {
                    "field": _("job position"),
                },
            )
            raise ValueError("jobpositions_not_found")

        list_permissions: list[str] = []

        for x in request.POST.keys():
            if x == "csrfmiddlewaretoken":
                continue
            elif request.POST[x] == "nopermission":
                continue

            permissionsod_split = x.split("_")
            permissionsod_0: str = permissionsod_split[0]
            permissionsod_1: str = permissionsod_split[1]
            permission_sod: str = f"{permissionsod_0}_{permissionsod_1}"

            if permission_sod not in list_permissions:
                list_permissions.append(permission_sod)

        for xx in range(0, len(list_permissions) - 1):
            permission_check: str = list_permissions[xx]
            permissions_check: list[str] = list_permissions[xx + 1 :]  # noqa

            for xxx in permissions_check:
                try:
                    appmodels.ApplicationPermissionsSoD.objects.get(
                        permission_sod=f"{permission_check}_{xxx}",
                    )
                    djangomessages.error(
                        request=request,
                        message=_(
                            "(%(field)s conflit) %(permission1)s"  # noqa
                        )
                        % {
                            "field": "sod",
                            "permission1": permission_check,
                        },
                    )
                    djangomessages.error(
                        request=request,
                        message=_(
                            "(%(field)s conflit) %(permission2)s"  # noqa
                        )
                        % {
                            "field": "sod",
                            "permission2": xxx,
                        },
                    )
                    raise ValueError("sod_conflit")

                except appmodels.ApplicationPermissionsSoD.DoesNotExist:
                    ...

        model_jobpositions: appmodels.ApplicationJobPositions
        model_jobpositions = (
            appmodels.ApplicationJobPositions.objects.get(  # noqa: E501
                id=codejobposition,
            )
        )

        appmodels.ApplicationPermissions.objects.filter(
            jobposition=codejobposition,
        ).delete()

        list_model_permissions: list[appmodels.ApplicationPermissions]
        list_model_permissions = []

        list_permissions = []

        for x in request.POST.keys():
            if x == "csrfmiddlewaretoken":
                continue
            elif request.POST[x] == "nopermission":
                continue

            permission_split = x.split("_")
            permission: list[str]
            permission = []

            for y in permission_split:
                permission.append(y)

                permission_describe: str
                permission_describe = (
                    f"{'_'.join(permission)}:{request.POST[x]}"  # noqa: E501
                )

                if permission_describe not in list_permissions:
                    list_permissions.append(permission_describe)

                    model_permissions: appmodels.ApplicationPermissions
                    model_permissions = appmodels.ApplicationPermissions()  # noqa: E501
                    model_permissions.jobposition = model_jobpositions
                    model_permissions.permission = permission_describe

                    if request.POST[x] == "edit":
                        permission_describe = (
                            f"{'_'.join(permission)}:view"  # noqa: E501
                        )
                        list_permissions.append(permission_describe)

                        view_model_permissions = (
                            appmodels.ApplicationPermissions()
                        )  # noqa: E501
                        view_model_permissions.jobposition = (
                            model_jobpositions  # noqa: E501
                        )
                        view_model_permissions.permission = (
                            permission_describe  # noqa: E501
                        )
                        list_model_permissions.append(view_model_permissions)

                    # mantido aqui para que o edit seja selecionado no html
                    list_model_permissions.append(model_permissions)

        appmodels.ApplicationPermissions.objects.bulk_create(
            list_model_permissions,
        )

        djangomessages.success(
            request=request,
            message=_("%(field)s successfully saved")
            % {
                "field": _("permission"),
            },
        )

        return redirect(
            "app:application:permissions:code:view",
            codejobposition=codejobposition,
        )

    except ValueError as e:
        if str(e) in ("jobpositions_not_found",):
            return redirect(
                "app:application:permissions:page",
            )

        elif str(e) in ("sod_conflit",):
            return redirect(
                "app:application:permissions:code:edit",
                codejobposition=codejobposition,
            )

        raise ValueError(e)
