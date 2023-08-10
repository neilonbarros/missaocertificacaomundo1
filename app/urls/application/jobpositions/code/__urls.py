from django.urls import include, path

from app import components as appcomponents

from . import remove

urls = (
    [
        path(
            route="",
            kwargs={"type_page": "view"},
            view=appcomponents.application.jobpositions.code.get.page,  # noqa: E501
            name="view",
        ),
        path(
            route="edit",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.jobpositions.code.get.page,  # noqa: E501
            name="edit",
        ),
        path(
            route="save",
            kwargs={"type_page": "edit"},
            view=appcomponents.application.jobpositions.code.post.save,  # noqa: E501
            name="save",
        ),
        path("remove/", include(remove.urls)),
    ],
    "code",
)
