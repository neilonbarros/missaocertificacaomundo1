from django.conf import settings
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _


def custom_page_not_found_view(request, exception):
    title: str = "404"  # type: ignore
    subtitle: str = "Not Found"  # type: ignore
    message_error: str = _("The requested page could not be found.")  # type: ignore # noqa
    return render(
        request=request,
        template_name="app/errors/_page.html",
        context={
            "settings_debug": settings.DEBUG,
            "html_language": translation.get_language(),
            "title": title,
            "menu": False,
            "display_center": True,
            "subtitle": subtitle,
            "message_error": message_error,
        },
    )
