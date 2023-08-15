from django.db import models as djangomodels


class ApplicationPermissionsSoD(djangomodels.Model):
    id = djangomodels.BigAutoField(
        editable=False,
        primary_key=True,
        null=False,
        unique=True,
    )
    permission_sod = djangomodels.CharField(
        blank=False,
        null=False,
        max_length=250,
    )

    class Meta:
        db_table = "app_permissions_sod"
