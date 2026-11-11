from apps.tags.models import Tag, TagStatus


# =====================================================
# TAG
# =====================================================

def get_tag(tag_id):
    """
    Devuelve una etiqueta por su ID.
    """

    return (
        Tag.objects
        .select_related(
            "company",
            "asset",
        )
        .filter(
            pk=tag_id,
        )
        .first()
    )


def get_tag_by_uuid(tag_uuid):
    """
    Devuelve una etiqueta por UUID.
    """

    return (
        Tag.objects
        .select_related(
            "company",
            "asset",
        )
        .filter(
            uuid=tag_uuid,
        )
        .first()
    )


def get_tag_by_short_code(
    *,
    company,
    short_code,
):
    """
    Devuelve una etiqueta mediante su código corto.
    """

    return (
        Tag.objects
        .select_related(
            "company",
            "asset",
        )
        .filter(
            company=company,
            short_code=short_code,
        )
        .first()
    )


# =====================================================
# COMPANY
# =====================================================

def get_company_tags(company):
    """
    Devuelve todas las etiquetas de una empresa.
    """

    return (
        Tag.objects
        .filter(
            company=company,
        )
        .select_related(
            "asset",
        )
        .order_by(
            "short_code",
        )
    )


def get_company_available_tags(company):
    """
    Etiquetas disponibles.
    """

    return get_company_tags(company).filter(
        status=TagStatus.AVAILABLE,
    )


def get_company_assigned_tags(company):
    """
    Etiquetas asignadas.
    """

    return get_company_tags(company).filter(
        status=TagStatus.ASSIGNED,
    )


# =====================================================
# ASSET
# =====================================================

def get_asset_tag(asset):
    """
    Devuelve la etiqueta asociada a un activo.
    """

    return (
        Tag.objects
        .filter(
            asset=asset,
        )
        .first()
    )


# =====================================================
# STATUS
# =====================================================

def get_tags_by_status(
    *,
    company,
    status,
):
    """
    Devuelve las etiquetas de una empresa
    filtradas por estado.
    """

    return (
        Tag.objects
        .filter(
            company=company,
            status=status,
        )
        .order_by(
            "short_code",
        )
    )


# =====================================================
# PUBLIC
# =====================================================

def get_public_tags(company):
    """
    Etiquetas públicas.
    """

    return (
        Tag.objects
        .filter(
            company=company,
            is_public=True,
        )
    )