from django.conf import settings
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _


def custom_permission_denied_view(request, exception=None):
    title: str = "403"  # type: ignore
    subtitle: str = "Forbidden"  # type: ignore
    message_error: str = _("You do not have permission to access.")  # type: ignore # noqa
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
