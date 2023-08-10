from django.db import models as djangomodels
from django.utils.translation import gettext_lazy as _

from app import models as appmodels


class ApplicationPermissions(djangomodels.Model):
    id = djangomodels.BigAutoField(
        editable=False,
        primary_key=True,
        null=False,
        unique=True,
    )
    permission = djangomodels.CharField(
        blank=False,
        null=False,
        max_length=150,
    )
    jobposition = djangomodels.ForeignKey(
        appmodels.ApplicationJobPositions,
        on_delete=djangomodels.CASCADE,
        blank=False,
        default=None,
        null=False,
        verbose_name=_("permission"),
        help_text=_("Inform the %(field)s")
        % {
            "field": _("permission"),
        },
    )

    class Meta:
        db_table = "app_permissions"
