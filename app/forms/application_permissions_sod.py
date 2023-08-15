from typing import Any

from django import forms as djangoforms
from django.utils.translation import gettext_lazy as _


class ApplicationPermissionsSoD(djangoforms.Form):
    permission1 = djangoforms.CharField(
        label=f"{_('permission').capitalize()} 1",
        required=True,
        help_text=_("select").capitalize(),
    )
    permission2 = djangoforms.CharField(
        label=f"{_('permission').capitalize()} 2",
        required=True,
        help_text=_("select").capitalize(),
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        permission1 = self.cleaned_data.get("permission1", None)
        permission2 = self.cleaned_data.get("permission2", None)

        if permission1 is not None and permission2 is not None:
            if permission1 == permission2:
                message: str = _("identical fields")
                self.add_error("permission1", message)
                self.add_error("permission2", message)

        return cleaned_data
