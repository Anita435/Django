from django.db import models

from .managers import ModelManager


class StatusMixin(models.Model):
    is_active = models.BooleanField("active", default=True)
    is_deleted = models.BooleanField("deleted", default=False)

    objects = ModelManager()

    class Meta:
        abstract = True