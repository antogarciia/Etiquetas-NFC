from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.common.models import BaseModel

from apps.common.constants import (
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    REFERENCE_MAX_LENGTH,
    ADDRESS_MAX_LENGTH,
    POSTAL_CODE_MAX_LENGTH,
    CITY_MAX_LENGTH,
    PROVINCE_MAX_LENGTH,
    COUNTRY_MAX_LENGTH,
    DEFAULT_COUNTRY,
)

from apps.companies.models import Company
from apps.accounts.models import User

from .category import AssetCategory



class AssetStatus(models.TextChoices):

    AVAILABLE = "available", "Disponible"

    RESERVED = "reserved", "Reservado"

    SOLD = "sold", "Vendido"

    RENTED = "rented", "Alquilado"

    MAINTENANCE = "maintenance", "Mantenimiento"

    ARCHIVED = "archived", "Archivado"




class Asset(BaseModel):

    """
    Activo perteneciente a una empresa.
    """


    # =====================================================
    # RELACIONES
    # =====================================================

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="assets",
    )


    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.PROTECT,
        related_name="assets",
    )


    responsible_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_assets",
        null=True,
        blank=True,
    )



    # =====================================================
    # IDENTIFICACIÓN
    # =====================================================


    asset_code = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )


    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )


    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        editable=False,
    )


    internal_reference = models.CharField(
        max_length=REFERENCE_MAX_LENGTH,
        blank=True,
    )



    # =====================================================
    # INFORMACIÓN
    # =====================================================


    description = models.TextField(
        blank=True,
    )


    address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        blank=True,
    )


    postal_code = models.CharField(
        max_length=POSTAL_CODE_MAX_LENGTH,
        blank=True,
    )


    city = models.CharField(
        max_length=CITY_MAX_LENGTH,
        blank=True,
    )


    province = models.CharField(
        max_length=PROVINCE_MAX_LENGTH,
        blank=True,
    )


    country = models.CharField(
        max_length=COUNTRY_MAX_LENGTH,
        default=DEFAULT_COUNTRY,
    )


    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )


    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )



    # =====================================================
    # ESTADO
    # =====================================================


    status = models.CharField(
        max_length=20,
        choices=AssetStatus.choices,
        default=AssetStatus.AVAILABLE,
    )



    # =====================================================
    # PUBLICACIÓN
    # =====================================================


    is_public = models.BooleanField(
        default=True,
    )


    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )


    is_featured = models.BooleanField(
        default=False,
    )



    # =====================================================
    # PRECIO
    # =====================================================


    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )


    currency = models.CharField(
        max_length=3,
        default="EUR",
    )


    available_from = models.DateField(
        null=True,
        blank=True,
    )



    # =====================================================
    # REPRESENTATION
    # =====================================================


    def __str__(self):

        return (
            f"{self.asset_code} - {self.name}"
        )



        # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def has_tag(self):
        """
        Indica si el activo tiene una etiqueta NFC asociada.
        """

        return hasattr(
            self,
            "tag"
        )


    @property
    def is_available(self):
        """
        Indica si el activo está disponible.
        """

        return self.status == AssetStatus.AVAILABLE


    @property
    def is_archived(self):
        """
        Indica si el activo está archivado.
        """

        return self.status == AssetStatus.ARCHIVED


    @property
    def cover_image(self):
        """
        Devuelve la imagen de portada.

        Si no existe una portada marcada,
        devuelve la primera imagen disponible.
        """

        image = self.images.filter(
            is_cover=True
        ).first()

        if image:
            return image

        return self.images.first()


    @property
    def gallery(self):
        """
        Devuelve todas las imágenes
        ordenadas por display_order.
        """

        return self.images.all()


    @property
    def image_count(self):
        """
        Número de imágenes asociadas.
        """

        return self.images.count()



    # =====================================================
    # NORMALIZATION
    # =====================================================


    def _normalize_fields(self):

        if self.name:

            self.name = (
                self.name
                .strip()
                .title()
            )


        if self.city:

            self.city = (
                self.city
                .strip()
                .title()
            )


        if self.province:

            self.province = (
                self.province
                .strip()
                .title()
            )


        if self.country:

            self.country = (
                self.country
                .strip()
                .title()
            )


        if self.address:

            self.address = (
                self.address
                .strip()
            )


        if self.internal_reference:

            self.internal_reference = (
                self.internal_reference
                .strip()
                .upper()
            )



    # =====================================================
    # GENERATORS
    # =====================================================


    def _generate_code(self):

        if not self.asset_code:


            last_asset = (
                Asset.all_objects
                .order_by("-id")
                .first()
            )


            number = (

                last_asset.id + 1

                if last_asset

                else 1

            )


            self.asset_code = (
                f"AST-{number:06d}"
            )



    def _generate_slug(self):

        base_slug = slugify(
            self.name
        )


        slug = base_slug

        counter = 2


        while (
            Asset.all_objects
            .filter(
                company=self.company,
                slug=slug,
            )
            .exclude(
                id=self.id,
            )
            .exists()
        ):

            slug = (
                f"{base_slug}-{counter}"
            )

            counter += 1


        self.slug = slug



    def _update_publication_date(self):

        if self.is_public:

            if not self.published_at:

                self.published_at = timezone.now()


        else:

            self.published_at = None




    # =====================================================
    # BUSINESS METHODS
    # =====================================================


    def publish(self):

        self.is_public = True
        self.published_at = timezone.now()

        self.save()



    def unpublish(self):

        self.is_public = False
        self.published_at = None

        self.save()



    def feature(self):

        self.is_featured = True

        self.save()



    def remove_feature(self):

        self.is_featured = False

        self.save()



    def archive(self):

        self.status = AssetStatus.ARCHIVED

        self.save()



    def activate(self):

        self.status = AssetStatus.AVAILABLE
        self.is_active = True

        self.save()



    # =====================================================
    # VALIDATION
    # =====================================================


    def clean(self):

        super().clean()


        if self.category:

            if self.category.company != self.company:

                raise ValidationError(
                    {
                        "category":
                        "La categoría pertenece a otra empresa."
                    }
                )



        if self.responsible_user:

            if self.responsible_user.company != self.company:

                raise ValidationError(
                    {
                        "responsible_user":
                        "El usuario pertenece a otra empresa."
                    }
                )



        if self.price is not None:

            if self.price < 0:

                raise ValidationError(
                    {
                        "price":
                        "El precio no puede ser negativo."
                    }
                )



        if self.latitude:

            if not -90 <= self.latitude <= 90:

                raise ValidationError(
                    {
                        "latitude":
                        "Latitud incorrecta."
                    }
                )



        if self.longitude:

            if not -180 <= self.longitude <= 180:

                raise ValidationError(
                    {
                        "longitude":
                        "Longitud incorrecta."
                    }
                )



    # =====================================================
    # SAVE
    # =====================================================


    def save(
        self,
        *args,
        **kwargs
    ):


        self._normalize_fields()

        self._generate_code()

        self._generate_slug()

        self._update_publication_date()

        self.full_clean()


        super().save(
            *args,
            **kwargs
        )



    # =====================================================
    # META
    # =====================================================


    class Meta:

        verbose_name = "Activo"

        verbose_name_plural = "Activos"


        ordering = [
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
                    "status",
                ]
            ),

            models.Index(
                fields=[
                    "asset_code",
                ]
            ),

            models.Index(
                fields=[
                    "slug",
                ]
            ),

        ]


        constraints = [

            models.UniqueConstraint(
                fields=[
                    "company",
                    "slug",
                ],
                name="unique_asset_slug_per_company",
            ),


            models.UniqueConstraint(
                fields=[
                    "company",
                    "internal_reference",
                ],
                name="unique_asset_reference_per_company",
            ),

        ]