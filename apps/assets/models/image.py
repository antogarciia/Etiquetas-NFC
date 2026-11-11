import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import BaseModel

from .asset import Asset


class AssetImage(BaseModel):
    """
    Imagen perteneciente a un activo.
    """

    # =====================================================
    # RELACIONES
    # =====================================================

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="images",
    )

    # =====================================================
    # IDENTIFICACIÓN
    # =====================================================

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    # =====================================================
    # IMAGEN
    # =====================================================

    image = models.ImageField(
        upload_to="assets/",
    )

    title = models.CharField(
        max_length=100,
        blank=True,
    )

    alt_text = models.CharField(
        max_length=150,
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    is_cover = models.BooleanField(
        default=False,
    )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __str__(self):

        return f"{self.asset.name} - {self.title or self.pk}"

    # =====================================================
    # PRIVATE METHODS
    # =====================================================

    def _normalize_fields(self):

        if self.title:

            self.title = self.title.strip()

        if self.alt_text:

            self.alt_text = self.alt_text.strip()

    # =====================================================
    # VALIDATION
    # =====================================================

    def clean(self):

        super().clean()

        if self.asset is None:

            raise ValidationError(
                {
                    "asset":
                    "Debe seleccionar un activo."
                }
            )

        if self.display_order < 0:

            raise ValidationError(
                {
                    "display_order":
                    "El orden no puede ser negativo."
                }
            )

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        self._normalize_fields()

        self.full_clean()

        # Primera imagen -> portada automática
        if not AssetImage.all_objects.filter(
            asset=self.asset,
            is_cover=True,
        ).exclude(
            pk=self.pk,
        ).exists():

            self.is_cover = True

        super().save(*args, **kwargs)

        # Solo una portada por activo
        if self.is_cover:

            (
                AssetImage.all_objects
                .filter(
                    asset=self.asset,
                )
                .exclude(
                    pk=self.pk,
                )
                .update(
                    is_cover=False,
                )
            )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, *args, **kwargs):

        asset = self.asset

        was_cover = self.is_cover

        super().delete(*args, **kwargs)

        if was_cover:

            replacement = (

                AssetImage.all_objects

                .filter(

                    asset=asset,

                    is_active=True,

                )

                .order_by(

                    "display_order",

                    "id",

                )

                .first()

            )

            if replacement:

                replacement.is_cover = True

                replacement.save(
                    update_fields=[
                        "is_cover",
                    ]
                )

    # =====================================================
    # BUSINESS METHODS
    # =====================================================

    def deactivate(self):

        was_cover = self.is_cover

        self.is_active = False

        self.is_cover = False

        self.save(
            update_fields=[
                "is_active",
                "is_cover",
            ]
        )

        if was_cover:

            replacement = (

                AssetImage.all_objects

                .filter(

                    asset=self.asset,

                    is_active=True,

                )

                .exclude(

                    pk=self.pk,

                )

                .order_by(

                    "display_order",

                    "id",

                )

                .first()

            )

            if replacement:

                replacement.is_cover = True

                replacement.save(
                    update_fields=[
                        "is_cover",
                    ]
                )

    def activate(self):

        self.is_active = True

        self.save(
            update_fields=[
                "is_active",
            ]
        )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        verbose_name = "Imagen"

        verbose_name_plural = "Imágenes"

        ordering = (
            "display_order",
            "id",
        )

        indexes = [

            models.Index(
                fields=[
                    "asset",
                ]
            ),

            models.Index(
                fields=[
                    "display_order",
                ]
            ),

            models.Index(
                fields=[
                    "is_cover",
                ]
            ),

        ]