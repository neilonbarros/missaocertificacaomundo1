from django.urls import path

from app import components as appcomponents

app_name: str = "app"


urls = (
    [
        path(
            route="",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.departments.code.remove.get.page,  # noqa: E501
            name="page",
        ),
        path(
            route="post",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.departments.code.remove.post.remove,  # noqa: E501
            name="post",
        ),
    ],
    "remove",
)
