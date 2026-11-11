from django.db import transaction
from django.core.exceptions import ValidationError

from apps.tags.models import Tag


# ==========================================================
# PRIVATE
# ==========================================================

def _generate_short_code(company):
    """
    Genera el siguiente código corto de una empresa.

    Ejemplo:

        GAR-000001
        GAR-000002
        GAR-000003
    """

    prefix = company.name[:3].upper()

    last_tag = (
    Tag.objects
    .filter(
        company=company,
    )
    .exclude(
        short_code="",
    )
    .order_by("-short_code")
    .first()
)

    if not last_tag:

        number = 1

    else:

        try:

            number = int(
                last_tag.short_code.split("-")[-1]
            ) + 1

        except Exception:

            number = 1

    return f"{prefix}-{number:06d}"


# ==========================================================
# CREATE
# ==========================================================

@transaction.atomic
def create_tag(
    *,
    company,
    asset=None,
    tag_type=None,
    is_public=True,
):

    tag = Tag(

        company=company,

        asset=asset,

        tag_type=tag_type or Tag.TagType.NTAG213,

        is_public=is_public,

    )

    tag.short_code = _generate_short_code(
        company,
    )

    tag.full_clean()

    tag.save()

    return tag


# ==========================================================
# ASSIGN
# ==========================================================

@transaction.atomic
def assign_asset(
    *,
    tag,
    asset,
):

    if asset.company != tag.company:

        raise ValidationError(
            "El activo pertenece a otra empresa."
        )

    tag.asset = asset

    tag.status = Tag.TagStatus.ASSIGNED

    tag.save(
        update_fields=[
            "asset",
            "status",
            "updated_at",
        ]
    )

    return tag


# ==========================================================
# REMOVE
# ==========================================================

@transaction.atomic
def unassign_asset(
    *,
    tag,
):

    tag.asset = None

    tag.status = Tag.TagStatus.AVAILABLE

    tag.save(
        update_fields=[
            "asset",
            "status",
            "updated_at",
        ]
    )

    return tag


# ==========================================================
# STATUS
# ==========================================================

@transaction.atomic
def change_status(
    *,
    tag,
    status,
):

    tag.status = status

    tag.full_clean()

    tag.save(
        update_fields=[
            "status",
            "updated_at",
            "deactivated_at",
        ]
    )

    return tag


# ==========================================================
# SCANS
# ==========================================================

@transaction.atomic
def register_scan(
    *,
    tag,
):

    tag.increment_scan_counter()

    return tag