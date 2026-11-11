import uuid

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.common.models import BaseModel
from apps.companies.models import Company
from apps.assets.models import Asset


class TagStatus(models.TextChoices):

    AVAILABLE = "available", "Disponible"

    ASSIGNED = "assigned", "Asignada"

    BLOCKED = "blocked", "Bloqueada"

    LOST = "lost", "Perdida"

    ARCHIVED = "archived", "Archivada"


class TagType(models.TextChoices):

    NTAG213 = "ntag213", "NTAG213"

    NTAG215 = "ntag215", "NTAG215"

    NTAG216 = "ntag216", "NTAG216"

    QR = "qr", "Código QR"

    OTHER = "other", "Otro"


class Tag(BaseModel):
    """
    Etiqueta NFC perteneciente a una empresa.
    """

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="tags",
    )

    asset = models.OneToOneField(
        Asset,
        on_delete=models.SET_NULL,
        related_name="tag",
        null=True,
        blank=True,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    short_code = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    status = models.CharField(
        max_length=20,
        choices=TagStatus.choices,
        default=TagStatus.AVAILABLE,
    )

    tag_type = models.CharField(
        max_length=20,
        choices=TagType.choices,
        default=TagType.NTAG213,
    )

    is_public = models.BooleanField(
        default=True,
    )

    scan_count = models.PositiveIntegerField(
        default=0,
    )

    last_scan_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    activated_at = models.DateTimeField(
        default=timezone.now,
    )

    deactivated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):

        return self.short_code

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def is_assigned(self):

        return self.status == TagStatus.ASSIGNED

    @property
    def is_available(self):

        return self.status == TagStatus.AVAILABLE

    @property
    def is_blocked(self):

        return self.status == TagStatus.BLOCKED

    @property
    def is_archived(self):

        return self.status == TagStatus.ARCHIVED

    # =====================================================
    # BUSINESS METHODS
    # =====================================================

    def assign_asset(self, asset):
        """
        Asigna el tag a un activo.
        """

        if self.status != TagStatus.AVAILABLE:

            raise ValidationError(
                "El tag no está disponible."
            )

        if asset.company != self.company:

            raise ValidationError(
                "El activo pertenece a otra empresa."
            )

        if hasattr(asset, "tag") and asset.tag != self:

            raise ValidationError(
                "Ese activo ya tiene otra etiqueta asignada."
            )

        self.asset = asset
        self.status = TagStatus.ASSIGNED

        self.save()

    def unassign_asset(self):
        """
        Libera el tag del activo.
        """

        self.asset = None
        self.status = TagStatus.AVAILABLE

        self.save()

    def increment_scan_counter(self):
        """
        Incrementa escaneos.
        """

        self.scan_count += 1
        self.last_scan_at = timezone.now()

        self.save(
            update_fields=[
                "scan_count",
                "last_scan_at",
                "updated_at",
            ]
        )

    # =====================================================
    # PRIVATE METHODS
    # =====================================================

    def generate_short_code(self):
        """
        Genera código NFC único.
        """

        last_tag = (
            Tag.all_objects
            .order_by("-id")
            .first()
        )

        number = (
            last_tag.id + 1
            if last_tag
            else 1
        )

        return f"NFC-{number:06d}"

    def _normalize_fields(self):

        if self.notes:

            self.notes = self.notes.strip()

    def _update_dates(self):

        if self.status in (
            TagStatus.BLOCKED,
            TagStatus.LOST,
            TagStatus.ARCHIVED,
        ):

            if self.deactivated_at is None:

                self.deactivated_at = timezone.now()

        else:

            self.deactivated_at = None

    # =====================================================
    # VALIDATION
    # =====================================================

    def clean(self):

        super().clean()

        if self.asset:

            if self.asset.company != self.company:

                raise ValidationError(
                    {
                        "asset":
                        "El activo pertenece a otra empresa."
                    }
                )

        if self.status == TagStatus.ASSIGNED and not self.asset:

            raise ValidationError(
                {
                    "asset":
                    "Un tag asignado debe tener un activo."
                }
            )

        if self.status == TagStatus.AVAILABLE and self.asset:

            raise ValidationError(
                {
                    "status":
                    "Un tag disponible no puede tener activo asociado."
                }
            )

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        if not self.short_code:

            self.short_code = self.generate_short_code()

        self._normalize_fields()
        self._update_dates()

        self.full_clean()

        super().save(*args, **kwargs)

    # =====================================================
    # META
    # =====================================================

    class Meta:

        verbose_name = "Etiqueta NFC"

        verbose_name_plural = "Etiquetas NFC"

        ordering = [
            "short_code",
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
                    "uuid",
                ]
            ),

            models.Index(
                fields=[
                    "is_public",
                ]
            ),

            models.Index(
                fields=[
                    "asset",
                ]
            ),

        ]