from django.urls import include, path

from app import components as appcomponents

from . import remove

urls = (
    [
        path(
            route="",
            view=appcomponents.application.permissions.sod.get.page,  # noqa: E501
            name="page",
        ),
        path(
            route="save",
            view=appcomponents.application.permissions.sod.post.save,  # noqa: E501
            name="save",
        ),
        path(
            route="export/csv",
            view=appcomponents.application.permissions.sod.export.mycsv,  # noqa: E501
            name="export_csv",
        ),
        path(
            route="export/xlsx",
            view=appcomponents.application.permissions.sod.export.myxlsx,  # noqa: E501
            name="export_xlsx",
        ),
        path("<int:codesod>/", include(remove.urls)),
    ],
    "sod",
)
