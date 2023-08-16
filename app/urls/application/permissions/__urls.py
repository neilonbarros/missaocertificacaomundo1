from django.urls import include, path

from app import components as appcomponents

from . import code, sod

urls = (
    [
        path(
            route="search",
            view=appcomponents.application.permissions.post.search,  # noqa: E501
            name="search",
        ),
        path(
            route="",
            view=appcomponents.application.permissions.get.page,
            name="page",
        ),
        path(
            route="export/csv",
            view=appcomponents.application.permissions.export.mycsv,  # noqa: E501
            name="export_csv",
        ),
        path(
            route="export/xlsx",
            view=appcomponents.application.permissions.export.myxlsx,  # noqa: E501
            name="export_xlsx",
        ),
        path("<int:codejobposition>/", include(code.urls)),
        path("sod/", include(sod.urls)),
    ],
    "permissions",
)
