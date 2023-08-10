from django.urls import path

from app import components as appcomponents

urls = (
    [
        path(
            route="",
            view=appcomponents.signup.get.page,
            name="page",
        ),
        path(
            route="post/",
            view=appcomponents.signup.post.signup,
            name="post",
        ),
    ],
    "signup",
)
