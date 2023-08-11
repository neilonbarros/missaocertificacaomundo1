from django import forms as djangoforms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from app import packages as apppackages


class SignUp(djangoforms.Form):
    cpf = djangoforms.CharField(
        max_length=11,
        min_length=11,
        label="cpf",
        required=True,
    )
    password_provisional = djangoforms.CharField(
        label=_("password provisional"),
        required=True,
    )
    password = djangoforms.CharField(
        label=_("password"),
        required=True,
    )

    def clean_cpf(self):
        data = self.cleaned_data["cpf"]

        if data is not None:
            try:
                data = apppackages.doc_br.validate_cpf(value=data)  # noqa: E501

            except ValueError as e:
                raise ValidationError(str(e))

        return data
