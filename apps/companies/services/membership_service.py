from django.db import transaction
from django.core.exceptions import ValidationError

from apps.companies.models import CompanyMembership
from apps.companies.models.membership import ROLE_CHOICES


@transaction.atomic
def add_member(
    *,
    company,
    user,
    role=ROLE_CHOICES.VIEWER,
):
    """
    Añade un usuario a una empresa.
    """

    membership = CompanyMembership.objects.filter(
        company=company,
        user=user,
    ).first()

    if membership:

        raise ValidationError(
            "El usuario ya pertenece a esta empresa."
        )

    return CompanyMembership.objects.create(
        company=company,
        user=user,
        role=role,
        is_active=True,
    )


@transaction.atomic
def remove_member(
    *,
    membership,
):
    """
    Elimina un miembro de una empresa.
    Nunca puede eliminar al propietario.
    """

    if membership.role == ROLE_CHOICES.OWNER:

        raise ValidationError(
            "No se puede eliminar al propietario de la empresa."
        )

    membership.delete()


@transaction.atomic
def change_member_role(
    *,
    membership,
    new_role,
):
    """
    Cambia el rol de un miembro.
    """

    if membership.role == ROLE_CHOICES.OWNER:

        raise ValidationError(
            "El propietario solo puede cambiarse mediante transfer_ownership()."
        )

    membership.role = new_role

    membership.full_clean()

    membership.save(
        update_fields=[
            "role",
            "updated_at",
        ]
    )

    return membership


@transaction.atomic
def activate_member(
    *,
    membership,
):
    """
    Activa un miembro.
    """

    membership.is_active = True

    membership.save(
        update_fields=[
            "is_active",
            "updated_at",
        ]
    )

    return membership


@transaction.atomic
def deactivate_member(
    *,
    membership,
):
    """
    Desactiva un miembro.
    """

    if membership.role == ROLE_CHOICES.OWNER:

        raise ValidationError(
            "No se puede desactivar el propietario."
        )

    membership.is_active = False

    membership.save(
        update_fields=[
            "is_active",
            "updated_at",
        ]
    )

    return membership