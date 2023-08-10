from django.urls import path

from app import components as appcomponents

app_name: str = "app"


urls = (
    [
        path(
            route="",
            view=appcomponents.signout.get.page,
            name="page",
        ),
        path(
            route="post/",
            view=appcomponents.signout.post.signout,
            name="post",
        ),
    ],
    "signout",
)
