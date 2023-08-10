from django.urls import include, path

from app import components as appcomponents

from . import code

app_name: str = "app"


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
        path("<str:codejobposition>/", include(code.urls)),
    ],
    "jobpositions",
)
