from django.urls import include, path

from app import components as appcomponents
from . import password

urls = (
    [
        path(
            route="",
            view=appcomponents.application.configuration.get.page,
            name="page",
        ),
        path("password/", include(password.urls)),
    ],
    "configuration",
)
