from django.conf import settings
from django.db import models

from apps.common.models import BaseModel

from django.core.exceptions import ValidationError


class ROLE_CHOICES(models.TextChoices):

    OWNER = "owner", "Propietario"
    ADMIN = "admin", "Administrador"
    EDITOR = "editor", "Editor"
    VIEWER = "viewer", "Solo lectura"


class CompanyMembership(BaseModel):
    """
    Relación entre usuarios y empresas.
    Define el rol y permisos del usuario dentro de una empresa.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_memberships",
    )

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES.choices,
        default=ROLE_CHOICES.VIEWER,
    )

    is_active = models.BooleanField(
        default=True,
    )



    def clean(self):

        super().clean()

        # ----------------------------------
        # Solo un owner activo por empresa
        # ----------------------------------

        if self.role == ROLE_CHOICES.OWNER and self.is_active:

            existing_owner = CompanyMembership.objects.filter(
                company=self.company,
                role=ROLE_CHOICES.OWNER,
                is_active=True,
            ).exclude(
                pk=self.pk,
            ).exists()

            if existing_owner:
                raise ValidationError(
                    "La empresa ya tiene un propietario activo."
                )


        # ----------------------------------
        # No dejar empresa sin owner activo
        # ----------------------------------

        if self.pk:

            previous = CompanyMembership.objects.get(
                pk=self.pk,
            )

            removing_owner = (
                previous.role == ROLE_CHOICES.OWNER
                and previous.is_active
                and (
                    self.role != ROLE_CHOICES.OWNER
                    or not self.is_active
                )
            )

            if removing_owner:

                remaining_owner = CompanyMembership.objects.filter(
                    company=self.company,
                    role=ROLE_CHOICES.OWNER,
                    is_active=True,
                ).exclude(
                    pk=self.pk,
                ).exists()

                if not remaining_owner:
                    raise ValidationError(
                        "No se puede eliminar o desactivar el último propietario activo de la empresa."
                    )
    # -------------------------
    # Representación
    # -------------------------

    def __str__(self):

        return f"{self.user.email} - {self.company.name}"


    # -------------------------
    # Roles básicos
    # -------------------------

    def is_owner(self):

        return self.role == ROLE_CHOICES.OWNER


    def is_admin(self):

        return self.role in (
            ROLE_CHOICES.OWNER,
            ROLE_CHOICES.ADMIN,
        )


    # -------------------------
    # Permisos empresa
    # -------------------------

    def can_manage_company(self):

        return self.role in (
            ROLE_CHOICES.OWNER,
            ROLE_CHOICES.ADMIN,
        )


    def can_manage_members(self):

        """
        Puede gestionar usuarios de la empresa.
        """

        return self.role in (
            ROLE_CHOICES.OWNER,
            ROLE_CHOICES.ADMIN,
        )


    def can_change_roles(self):

        """
        Solo el propietario puede cambiar roles.
        """

        return self.role == ROLE_CHOICES.OWNER


    def can_delete_company(self):

        """
        Solo el propietario puede eliminar la empresa.
        """

        return self.role == ROLE_CHOICES.OWNER


    # -------------------------
    # Permisos activos
    # -------------------------

    def can_manage_assets(self):

        return self.role in (
            ROLE_CHOICES.OWNER,
            ROLE_CHOICES.ADMIN,
            ROLE_CHOICES.EDITOR,
        )


    def can_delete_assets(self):

        return self.role in (
            ROLE_CHOICES.OWNER,
            ROLE_CHOICES.ADMIN,
        )


    def can_publish_assets(self):

        return self.role in (
            ROLE_CHOICES.OWNER,
            ROLE_CHOICES.ADMIN,
            ROLE_CHOICES.EDITOR,
        )


    def can_view(self):

        return self.is_active


    class Meta:

        verbose_name = "Membresía de empresa"

        verbose_name_plural = "Membresías de empresa"

        ordering = [
            "company",
            "role",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "company",
                    "user",
                ],
                name="unique_company_user",
            ),

        ]