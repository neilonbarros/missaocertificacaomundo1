from django.urls import path

from app import components as appcomponents

urls = (
    [
        path(
            route="",
            kwargs={"type_page": "view"},
            view=appcomponents.application.permissions.code.get.page,  # noqa: E501
            name="view",
        ),
        path(
            route="edit",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.permissions.code.get.page,  # noqa: E501
            name="edit",
        ),
        path(
            route="save",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.permissions.code.post.save,  # noqa: E501
            name="save",
        ),
    ],
    "code",
)
