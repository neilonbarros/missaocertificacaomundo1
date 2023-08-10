from django.urls import include, path

from app import components as appcomponents

from . import code

urls = (
    [
        path(
            route="search",
            view=appcomponents.application.departments.post.search,  # noqa: E501
            name="search",
        ),
        path(
            route="",
            view=appcomponents.application.departments.get.page,
            name="page",
        ),
        path("<str:codedepartment>/", include(code.urls)),
    ],
    "departments",
)
