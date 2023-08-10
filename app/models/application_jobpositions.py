from django.core.validators import MinLengthValidator
from django.db import models as djangomodels
from django.utils.translation import gettext_lazy as _

from app import models as appmodels


class ApplicationJobPositions(djangomodels.Model):
    id = djangomodels.BigAutoField(
        editable=False,
        primary_key=True,
        null=False,
        unique=True,
    )
    jobposition = djangomodels.CharField(
        max_length=150,
        blank=False,
        default=None,
        null=False,
        verbose_name=_("jobposition"),
        help_text=_("Minimum %(minimum_characters)s characters")
        % {
            "minimum_characters": str(5),
        },
        validators=[
            MinLengthValidator(5),
        ],
    )
    department = djangomodels.ForeignKey(
        appmodels.ApplicationDepartments,
        on_delete=djangomodels.CASCADE,
        blank=False,
        default=None,
        null=False,
        verbose_name=_("department"),
        help_text=_("Select"),
    )

    class Meta:
        db_table = "app_jobpositions"
        ordering = [
            "jobposition",
        ]

        unique_together = [
            [
                "department",
                "jobposition",
            ]
        ]
