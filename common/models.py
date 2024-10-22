from django.db import models


class CommonModel(models.Model):
    """Common Model Definition"""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )  # auto_now_'add' -> when data created
    updated_at = models.DateTimeField(
        auto_now=True,
    )  # auto_now -> when data updated

    class Meta:
        abstract = True
