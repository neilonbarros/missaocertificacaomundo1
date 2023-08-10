from django.core.validators import MinLengthValidator
from django.db import models as djangomodels
from django.utils.translation import gettext_lazy as _
from app import models as appmodels


class ApplicationPeoples(djangomodels.Model):
    id = djangomodels.BigAutoField(
        editable=False,
        primary_key=True,
        null=False,
        unique=True,
    )
    status = djangomodels.BooleanField(
        blank=False,
        default=False,
        null=False,
        verbose_name=_("status"),
    )
    cpf = djangomodels.CharField(
        blank=False,
        max_length=14,
        null=False,
        unique=True,
        verbose_name=_("cpf"),
        error_messages={
            "unique": _("This %(field)s already exists")
            % {
                "field": _("cpf"),
            },
        },
        help_text=_("Only numbers"),
    )
    fullname = djangomodels.CharField(
        max_length=150,
        blank=False,
        default=None,
        null=False,
        verbose_name=_("fullname"),
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
        on_delete=djangomodels.SET_NULL,
        blank=False,
        default=None,
        null=True,
        verbose_name=_("department"),
        help_text=_("Inform the %(field)s")
        % {
            "field": _("department"),
        },
    )
    jobposition = djangomodels.ForeignKey(
        appmodels.ApplicationJobPositions,
        on_delete=djangomodels.SET_NULL,
        blank=False,
        default=None,
        null=True,
        verbose_name=_("job position"),
        help_text=_("Inform the %(field)s")
        % {
            "field": _("job position"),
        },
    )

    class Meta:
        db_table = "app_peoples"
        ordering = [
            "fullname",
        ]
