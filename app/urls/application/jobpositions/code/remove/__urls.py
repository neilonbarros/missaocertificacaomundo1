from django.urls import path

from app import components as appcomponents

urls = (
    [
        path(
            route="",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.jobpositions.code.remove.get.page,  # noqa: E501
            name="page",
        ),
        path(
            route="post",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.jobpositions.code.remove.post.remove,  # noqa: E501
            name="post",
        ),
    ],
    "remove",
)
