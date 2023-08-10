from django.conf import settings
from django.shortcuts import render
from django.utils import translation

app_name: str = "app"


def custom_error_view(request, exception=None):
    title: str = "500"  # type: ignore
    subtitle: str = "Internal Server Error"  # type: ignore
    message_error: str = ""  # type: ignore # noqa
    return render(
        request=request,
        template_name="app/errors/_page.html",
        context={
            "settings_debug": settings.DEBUG,
            "app_name": app_name,
            "html_language": translation.get_language(),
            "title": title,
            "menu": False,
            "display_center": True,
            "subtitle": subtitle,
            "message_error": message_error,
        },
    )
