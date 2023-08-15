from django.urls import path

from app import components as appcomponents

urls = (
    [
        path(
            route="remove",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.permissions.sod.remove.get.page,  # noqa: E501
            name="page",
        ),
        path(
            route="post",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.permissions.sod.remove.post.remove,  # noqa: E501
            name="post",
        ),
    ],
    "remove",
)
