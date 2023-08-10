from django.urls import include, path

from app import components as appcomponents

from . import application, home, signin, signout, signup

app_name: str = "app"

urlpatterns = [
    path(
        route="",
        view=appcomponents.signin.get.page,
        name="",
    ),
    path("signin/", include(signin.urls)),
    path("signup/", include(signup.urls)),
    path("signout/", include(signout.urls)),
    path("home/", include(home.urls)),
    path("application/", include(application.urls)),
]
