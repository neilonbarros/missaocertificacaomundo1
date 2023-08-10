from django.urls import path

from app import components as appcomponents

urls = (
    [
        path(
            route="",
            view=appcomponents.home.get.page,
            name="page",
        ),
    ],
    "home",
)
