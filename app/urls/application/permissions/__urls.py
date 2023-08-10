from django.urls import include, path

from app import components as appcomponents

from . import code

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
        path("<int:codejobposition>/", include(code.urls)),
    ],
    "permissions",
)
