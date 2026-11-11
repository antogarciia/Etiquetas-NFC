from django.db import models

from apps.common.models import BaseModel

from apps.accounts.models import User

from apps.common.constants import (
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    PHONE_MAX_LENGTH,
    WEBSITE_MAX_LENGTH,
    ADDRESS_MAX_LENGTH,
    CITY_MAX_LENGTH,
    COUNTRY_MAX_LENGTH,
    DEFAULT_COUNTRY,
    DEFAULT_IS_ACTIVE,
)

INDUSTRY_CHOICES = [

    ("real_estate", "Inmobiliaria"),

    ("hotel", "Hotel"),

    ("restaurant", "Restaurante"),

    ("retail", "Comercio"),

    ("other", "Otro"),
]


class Company(BaseModel):
    """
    Empresa que utiliza la plataforma.
    """
    
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="owned_companies",
    )
    
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )
    
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
    )
    
    logo = models.ImageField(
    upload_to="companies/logos/",
    blank=True,
    null=True,
    )


    description = models.TextField(
        blank=True,
    )


    email = models.EmailField(
        blank=True,
    )


    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        blank=True,
    )


    website = models.URLField(
        blank=True,
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        blank=True,
    )


    city = models.CharField(
        max_length=CITY_MAX_LENGTH,
        blank=True,
    )


    country = models.CharField(
        max_length=COUNTRY_MAX_LENGTH,
        default=DEFAULT_COUNTRY,
    )

    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES,
        default="real_estate",
    )

    is_active = models.BooleanField(
        default=DEFAULT_IS_ACTIVE,
    )


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

        ordering = [
            "name",
        ]

        indexes = [
            models.Index(fields=["industry"]),
            models.Index(fields=["is_active"]),
        ]