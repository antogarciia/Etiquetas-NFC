from django.contrib import admin

from apps.tags.models import Tag


class TagInline(admin.StackedInline):
    """
    Gestión del Tag NFC asociado al activo.
    """

    model = Tag

    extra = 0

    max_num = 1

    can_delete = False


    readonly_fields = (

        "uuid",
        "short_code",
        "scan_count",
        "last_scan_at",
        "created_at",
        "updated_at",

    )


    fields = (

        "short_code",
        "uuid",
        "status",
        "tag_type",
        "is_public",
        "scan_count",
        "last_scan_at",
        "notes",
        "created_at",
        "updated_at",

    )


    verbose_name = "Etiqueta NFC"

    verbose_name_plural = "Etiqueta NFC asociada"