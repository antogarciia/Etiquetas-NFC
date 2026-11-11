from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from apps.common.models import BaseModel
from apps.companies.models import Company

from .icons import CategoryIcon

from apps.common.constants import (
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    COLOR_MAX_LENGTH,
    DEFAULT_COLOR,
)


class AssetCategory(BaseModel):
    """
    Categoría de activos perteneciente a una empresa.
    """


    # =====================================================
    # RELACIONES
    # =====================================================

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="asset_categories",
    )


    # =====================================================
    # INFORMACIÓN
    # =====================================================

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )


    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        editable=False,
    )


    description = models.TextField(
        blank=True,
    )


    color = models.CharField(
        max_length=COLOR_MAX_LENGTH,
        default=DEFAULT_COLOR,
    )


    icon_name = models.CharField(
        max_length=30,
        choices=CategoryIcon.choices,
        default=CategoryIcon.HOUSE,
    )


    display_order = models.PositiveIntegerField(
        default=0,
    )


    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __str__(self):

        return self.name


    # =====================================================
    # NORMALIZATION
    # =====================================================

    def _normalize_fields(self):

        if self.name:

            self.name = self.name.strip().title()


        if self.color:

            self.color = self.color.strip().upper()



    # =====================================================
    # VALIDATION
    # =====================================================

    def clean(self):

        super().clean()


        if not self.name:

            raise ValidationError(
                {
                    "name":
                    "El nombre de la categoría es obligatorio."
                }
            )


    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        self._normalize_fields()


        self.slug = slugify(
            self.name
        )


        self.full_clean()


        super().save(*args, **kwargs)



    # =====================================================
    # META
    # =====================================================

    class Meta:

        verbose_name = "Categoría de activo"

        verbose_name_plural = "Categorías de activos"


        ordering = [
            "display_order",
            "name",
        ]


        indexes = [

            models.Index(
                fields=[
                    "company",
                ]
            ),

            models.Index(
                fields=[
                    "slug",
                ]
            ),

            models.Index(
                fields=[
                    "is_active",
                ]
            ),

        ]


        constraints = [

            models.UniqueConstraint(
                fields=[
                    "company",
                    "name",
                ],
                name="unique_category_per_company",
            ),

            models.UniqueConstraint(
                fields=[
                    "company",
                    "slug",
                ],
                name="unique_category_slug_per_company",
            ),

        ]