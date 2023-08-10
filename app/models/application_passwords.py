from django.db import models as djangomodels
from django.utils.translation import gettext_lazy as _

from app import models as appmodels


class ApplicationPasswords(djangomodels.Model):
    id = djangomodels.BigAutoField(
        editable=False,
        primary_key=True,
        null=False,
        unique=True,
    )
    provisional = djangomodels.BooleanField(
        blank=False,
        default=False,
        null=False,
        verbose_name=_("provisional"),
    )
    salt = djangomodels.BinaryField(
        blank=False,
        null=False,
    )
    hashed = djangomodels.BinaryField(
        blank=False,
        null=False,
    )
    people = djangomodels.ForeignKey(
        appmodels.ApplicationPeoples,
        on_delete=djangomodels.CASCADE,
        blank=False,
        default=None,
        null=False,
    )

    class Meta:
        db_table = "app_passwords"
