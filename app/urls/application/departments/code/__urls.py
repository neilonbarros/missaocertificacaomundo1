from django.urls import include, path

from app import components as appcomponents

from . import remove

app_name: str = "app"


urls = (
    [
        path(
            route="",
            kwargs={"type_page": "view"},
            view=appcomponents.application.departments.code.get.page,  # noqa: E501
            name="view",
        ),
        path(
            route="edit",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.departments.code.get.page,  # noqa: E501
            name="edit",
        ),
        path(
            route="save",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.departments.code.post.save,  # noqa: E501
            name="save",
        ),
        path("remove/", include(remove.urls)),
    ],
    "code",
)
