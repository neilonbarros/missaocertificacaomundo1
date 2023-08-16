from django.urls import include, path

from app import components as appcomponents

from . import code

urls = (
    [
        path(
            route="search",
            view=appcomponents.application.peoples.post.search,  # noqa: E501
            name="search",
        ),
        path(
            route="",
            view=appcomponents.application.peoples.get.page,
            name="page",
        ),
        path(
            route="export/csv",
            view=appcomponents.application.peoples.export.mycsv,  # noqa: E501
            name="export_csv",
        ),
        path(
            route="export/xlsx",
            view=appcomponents.application.peoples.export.myxlsx,  # noqa: E501
            name="export_xlsx",
        ),
        path("<str:codepeople>/", include(code.urls)),
    ],
    "peoples",
)
