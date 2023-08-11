from django import forms as djangoforms
from django.utils.translation import gettext_lazy as _


class ConfigurationPassword(djangoforms.Form):
    password = djangoforms.CharField(
        label=_("password"),
        required=True,
    )
    password_new = djangoforms.CharField(
        label=_("new password"),
        required=True,
    )
    password_new_again = djangoforms.CharField(
        label=_("new password again"),
        required=True,
    )
