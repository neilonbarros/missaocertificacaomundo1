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
        path("<str:codepeople>/", include(code.urls)),
    ],
    "peoples",
)
