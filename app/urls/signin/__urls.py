from django.urls import path

from app import components as appcomponents

app_name: str = "app"


urls = (
    [
        path(
            route="",
            view=appcomponents.signin.get.page,
            name="page",
        ),
        path(
            route="post/",
            view=appcomponents.signin.post.signin,
            name="post",
        ),
    ],
    "signin",
)
