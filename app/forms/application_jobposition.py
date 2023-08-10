from typing import Any, Optional

from django import forms as djangoforms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

from app import models as appmodels


class ApplicationJobPositions(djangoforms.ModelForm):
    button_submit = djangoforms.CharField(
        required=False,
        min_length=1,
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        cleaned_data = self.name_clean(
            cleaned_data=cleaned_data,
        )
        return cleaned_data

    def name_clean(
        self,
        cleaned_data: dict[str, Any],
    ) -> dict[str, Any]:
        value: Optional[str] = cleaned_data.get("jobposition", None)

        if value is not None:
            name: str = value.lower().strip()
            cleaned_data["jobposition"] = name

        return cleaned_data

    class Meta:
        model = appmodels.ApplicationJobPositions
        fields = "__all__"
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": _("%(field_labels)s already exist."),
            }
        }
