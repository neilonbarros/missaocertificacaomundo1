from django.urls import path

from app import components as appcomponents

urls = (
    [
        path(
            route="save",
            view=appcomponents.application.configuration.password.post.save,  # noqa: E501
            name="save",
        ),
    ],
    "password",
)
