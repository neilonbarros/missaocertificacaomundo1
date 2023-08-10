from typing import Any, Optional

from django import forms as djangoforms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

from app import models as appmodels
from app import packages as apppackages


class ApplicationPeoples(djangoforms.ModelForm):
    button_submit = djangoforms.CharField(
        required=False,
        min_length=1,
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        cleaned_data = self.cpf_clean(
            cleaned_data=cleaned_data,
        )
        cleaned_data = self.fullname_clean(
            cleaned_data=cleaned_data,
        )
        return cleaned_data

    def cpf_clean(
        self,
        cleaned_data: dict[str, Any],
    ) -> dict[str, Any]:
        value: Optional[str] = cleaned_data.get("cpf", None)

        if value is not None:
            try:
                cleaned_data["cpf"] = apppackages.doc_br.validate_cpf(
                    value=value
                )  # noqa: E501

            except ValueError as e:
                self.add_error("cpf", str(e))

        return cleaned_data

    def fullname_clean(
        self,
        cleaned_data: dict[str, Any],
    ) -> dict[str, Any]:
        value: Optional[str] = cleaned_data.get("fullname", None)

        if value is not None:
            name: str = value.lower().strip()
            cleaned_data["fullname"] = name

        return cleaned_data

    class Meta:
        model = appmodels.ApplicationPeoples
        fields = [
            "jobposition",
            "cpf",
            "fullname",
            "status",
        ]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": _("%(field_labels)s already exist."),
            }
        }
