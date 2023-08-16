from django.urls import include, path

from app import components as appcomponents

from . import code

urls = (
    [
        path(
            route="search",
            view=appcomponents.application.jobpositions.post.search,  # noqa: E501
            name="search",
        ),
        path(
            route="",
            view=appcomponents.application.jobpositions.get.page,
            name="page",
        ),
        path(
            route="export/csv",
            view=appcomponents.application.jobpositions.export.mycsv,  # noqa: E501
            name="export_csv",
        ),
        path(
            route="export/xlsx",
            view=appcomponents.application.jobpositions.export.myxlsx,  # noqa: E501
            name="export_xlsx",
        ),
        path("<str:codejobposition>/", include(code.urls)),
    ],
    "jobpositions",
)
