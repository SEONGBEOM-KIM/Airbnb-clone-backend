from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    # AbstractUser first_name, last_name overriding
    first_name = models.CharField(
        max_length=150, editable=False
    )  # editable=False -> user cannot use
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
