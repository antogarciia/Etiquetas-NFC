from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.common.models import BaseModel

from .managers import UserManager

from apps.common.constants import (
    NAME_MAX_LENGTH,
    PHONE_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    TIMEZONE_MAX_LENGTH,
    DEFAULT_LANGUAGE,
    DEFAULT_TIMEZONE,
)


LANGUAGE_CHOICES = [
    ("es", "Español"),
    ("en", "English"),
]

TIMEZONE_CHOICES = [
    ("Europe/Madrid", "Europe/Madrid"),
    ("Europe/London", "Europe/London"),
]

class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        unique=True,
    )

    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    phone_number = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to="users/profile/",
        blank=True,
        null=True,
    )

    language = models.CharField(
        max_length=LANGUAGE_MAX_LENGTH,
        choices=LANGUAGE_CHOICES,
        default=DEFAULT_LANGUAGE,
    )

    timezone = models.CharField(
        max_length=TIMEZONE_MAX_LENGTH,
        choices=TIMEZONE_CHOICES,
        default=DEFAULT_TIMEZONE,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

        ordering = [
            "first_name",
            "last_name",
        ]