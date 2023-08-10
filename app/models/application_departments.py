from django.core.validators import MinLengthValidator
from django.db import models as djangomodels
from django.utils.translation import gettext_lazy as _


class ApplicationDepartments(djangomodels.Model):
    id = djangomodels.BigAutoField(
        editable=False,
        primary_key=True,
        null=False,
        unique=True,
    )
    department = djangomodels.CharField(
        unique=True,
        max_length=150,
        blank=False,
        default=None,
        null=False,
        verbose_name=_("department"),
        error_messages={
            "unique": _("This %(field)s already exists")
            % {
                "field": _("department"),
            },
        },
        help_text=_("Minimum %(minimum_characters)s characters")
        % {
            "minimum_characters": str(5),
        },
        validators=[
            MinLengthValidator(5),
        ],
    )

    class Meta:
        db_table = "app_departments"
        ordering = [
            "department",
        ]
