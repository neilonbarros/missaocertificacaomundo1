from typing import Any, Optional

from django import forms as djangoforms

from app import models as appmodels


class ApplicationDepartment(djangoforms.ModelForm):
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
        value: Optional[str] = cleaned_data.get("department", None)

        if value is not None:
            name: str = value.lower().strip()
            cleaned_data["department"] = name

        return cleaned_data

    class Meta:
        model = appmodels.ApplicationDepartments
        fields = "__all__"
