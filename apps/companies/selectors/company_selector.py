from django.db.models import Count

from apps.companies.models import Company, CompanyMembership
from apps.companies.models.membership import ROLE_CHOICES


# =====================================================
# COMPANY
# =====================================================

def get_company(company_id):
    """
    Devuelve una empresa por su ID.
    """

    return Company.objects.filter(
        pk=company_id,
    ).first()


def get_active_companies():
    """
    Devuelve todas las empresas activas.
    """

    return Company.objects.filter(
        is_active=True,
    ).order_by(
        "name",
    )


def get_user_companies(user):
    """
    Empresas activas a las que pertenece un usuario.
    """

    return Company.objects.filter(
        memberships__user=user,
        memberships__is_active=True,
    ).distinct()


def get_company_with_members(company_id):
    """
    Empresa con sus miembros precargados.
    """

    return (
        Company.objects
        .prefetch_related(
            "memberships",
        )
        .filter(
            pk=company_id,
        )
        .first()
    )


# =====================================================
# OWNER
# =====================================================

def get_company_owner(company):
    """
    Devuelve la membresía del propietario.
    """

    return CompanyMembership.objects.filter(
        company=company,
        role=ROLE_CHOICES.OWNER,
        is_active=True,
    ).first()


def is_company_owner(
    user,
    company,
):
    """
    Comprueba si un usuario es el propietario.
    """

    return CompanyMembership.objects.filter(
        company=company,
        user=user,
        role=ROLE_CHOICES.OWNER,
        is_active=True,
    ).exists()


# =====================================================
# ADMINS
# =====================================================

def get_company_admins(company):
    """
    Devuelve todos los administradores activos.
    """

    return CompanyMembership.objects.filter(
        company=company,
        role=ROLE_CHOICES.ADMIN,
        is_active=True,
    )


def get_company_editors(company):
    """
    Devuelve todos los editores activos.
    """

    return CompanyMembership.objects.filter(
        company=company,
        role=ROLE_CHOICES.EDITOR,
        is_active=True,
    )


def get_company_members(company):
    """
    Devuelve todos los miembros activos.
    """

    return CompanyMembership.objects.filter(
        company=company,
        is_active=True,
    ).select_related(
        "user",
    )


# =====================================================
# STATS
# =====================================================

def get_company_members_count(company):
    """
    Número de miembros activos.
    """

    return CompanyMembership.objects.filter(
        company=company,
        is_active=True,
    ).count()


def get_companies_with_member_count():
    """
    Empresas anotadas con el número de miembros.
    """

    return (
        Company.objects
        .annotate(
            total_members=Count(
                "memberships",
            )
        )
        .order_by(
            "name",
        )
    )


# =====================================================
# ASSETS
# =====================================================

def get_company_assets(company):
    """
    Devuelve los activos de una empresa.
    """

    return company.assets.all()