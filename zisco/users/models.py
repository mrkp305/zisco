from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from zisco.core.models import UUIDModel


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Customer(UUIDModel):
    name = models.CharField(
        max_length=255,
    )
    email = models.EmailField(
        null=True, blank=True,
    )
    address = models.CharField(
        null=True, blank=True,
        max_length=255
    )
    user = models.OneToOneField(
        to="users.User",
        related_name="profile",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "customers"

    def __str__(self):
        return self.name
