import re
from typing import Optional

from validate_docbr import CPF

from django.utils.translation import gettext_lazy as _


def validate_cpf(value: Optional[str]) -> str:
    if value is None:
        raise ValueError(
            _("The %(field)s is invalid")
            % {
                "field": _("cpf"),
            }
        )

    value = value.strip()
    value = re.sub(r"[^0-9]", "", value)
    value = str(value).rjust(11, "0")
    value = str(value)

    if CPF().validate(value) is False:
        raise ValueError(
            _("The %(field)s is invalid")
            % {
                "field": _("cpf"),
            }
        )
    return value
