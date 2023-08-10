import re
from typing import Optional

from validate_docbr import CNPJ

from django.utils.translation import gettext_lazy as _


def validate_cnpj(value: Optional[str]) -> str:
    if value is None:
        raise ValueError(
            _("The %(field)s is invalid")
            % {
                "field": _("cnpj"),
            }
        )

    value = value.strip()
    value = re.sub(r"[^0-9]", "", value)
    value = str(value).rjust(14, "0")

    if CNPJ().validate(value) is False:
        raise ValueError(
            _("The %(field)s is invalid")
            % {
                "field": _("cnpj"),
            }
        )
    return value
