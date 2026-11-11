from django.db import transaction
from django.core.exceptions import ValidationError

from apps.companies.models import CompanyMembership
from apps.companies.models.membership import ROLE_CHOICES



@transaction.atomic
def transfer_ownership(
    company,
    new_owner,
):
    """
    Transfiere la propiedad de una empresa
    a otro usuario existente.
    """


    current_owner = CompanyMembership.objects.filter(
        company=company,
        role=ROLE_CHOICES.OWNER,
        is_active=True,
    ).first()


    if not current_owner:

        raise ValidationError(
            "La empresa no tiene un propietario activo."
        )


    if current_owner.user == new_owner:

        raise ValidationError(
            "El nuevo propietario ya es el propietario actual."
        )


    # Comprobar que el nuevo propietario pertenece a la empresa

    new_membership = CompanyMembership.objects.filter(
        company=company,
        user=new_owner,
        is_active=True,
    ).first()


    if not new_membership:

        raise ValidationError(
            "El nuevo propietario debe ser miembro activo de la empresa."
        )


    # Nuevo owner

    new_membership.role = ROLE_CHOICES.OWNER

    new_membership.save(
        update_fields=[
            "role",
            "updated_at",
        ]
    )


    # Antiguo owner pasa a admin

    current_owner.role = ROLE_CHOICES.ADMIN

    current_owner.save(
        update_fields=[
            "role",
            "updated_at",
        ]
    )


    # Actualizar owner principal de Company

    company.owner = new_owner

    company.save(
        update_fields=[
            "owner",
            "updated_at",
        ]
    )


    return new_membership



