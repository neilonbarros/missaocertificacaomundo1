from django.urls import path, include

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
        path("<int:codesod>/", include(remove.urls)),
    ],
    "sod",
)
