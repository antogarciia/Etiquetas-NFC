from django.contrib import admin
from django.utils.html import format_html

from apps.assets.models import AssetImage


@admin.register(AssetImage)
class AssetImageAdmin(admin.ModelAdmin):

    # -------------------------------------------------
    # GENERAL
    # -------------------------------------------------

    list_per_page = 30

    ordering = (
        "asset",
        "display_order",
    )

    date_hierarchy = "created_at"

    # -------------------------------------------------
    # LIST
    # -------------------------------------------------

    list_display = (

        "preview",

        "asset_name",

        "title",

        "display_order",

        "cover",

        "active",

    )

    # -------------------------------------------------
    # FILTERS
    # -------------------------------------------------

    list_filter = (

        "is_cover",

        "is_active",

        "asset__company",

    )

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    search_fields = (

        "asset__name",

        "title",

        "alt_text",

    )

    # -------------------------------------------------
    # AUTOCOMPLETE
    # -------------------------------------------------

    autocomplete_fields = (

        "asset",

    )

    # -------------------------------------------------
    # READONLY
    # -------------------------------------------------

    readonly_fields = (

        "uuid",

        "preview_large",

        "created_at",

        "updated_at",

    )

    # -------------------------------------------------
    # FIELDSETS
    # -------------------------------------------------

    fieldsets = (

        (
            "Información",
            {
                "fields": (

                    "asset",

                    "image",

                    "preview_large",

                    "title",

                    "alt_text",

                ),
            },
        ),

        (
            "Configuración",
            {
                "fields": (

                    "display_order",

                    "is_cover",

                    "is_active",

                ),
            },
        ),

        (
            "Identificación",
            {
                "fields": (

                    "uuid",

                ),
            },
        ),

        (
            "Fechas",
            {
                "fields": (

                    "created_at",

                    "updated_at",

                ),
            },
        ),

    )

    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------

    @admin.display(
        description="Activo",
        ordering="asset",
    )
    def asset_name(self, obj):

        return obj.asset.name


    @admin.display(
        description="Portada",
        boolean=True,
    )
    def cover(self, obj):

        return obj.is_cover


    @admin.display(
        description="Activa",
        boolean=True,
        ordering="is_active",
    )
    def active(self, obj):

        return obj.is_active


    @admin.display(description="Miniatura")
    def preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" '
                'style="height:60px;'
                'width:90px;'
                'object-fit:cover;'
                'border-radius:8px;" />',
                obj.image.url,
            )

        return "-"


    @admin.display(description="Vista previa")
    def preview_large(self, obj):

        if obj.pk and obj.image:

            return format_html(
                '<img src="{}" '
                'style="max-height:350px;'
                'border-radius:12px;'
                'box-shadow:0 0 8px rgba(0,0,0,.15);" />',
                obj.image.url,
            )

        return "Sin imagen"

    # -------------------------------------------------
    # ACTIONS
    # -------------------------------------------------

    actions = (

        "mark_cover",

        "activate_images",

        "deactivate_images",

    )

    @admin.action(description="Marcar como portada")
    def mark_cover(self, request, queryset):

        for image in queryset:

            image.is_cover = True

            image.save()


    @admin.action(description="Activar imágenes")
    def activate_images(self, request, queryset):

        queryset.update(
            is_active=True,
        )


    @admin.action(description="Desactivar imágenes")
    def deactivate_images(self, request, queryset):

        queryset.update(
            is_active=False,
        )

    # -------------------------------------------------
    # PERMISOS
    # -------------------------------------------------

    def has_delete_permission(self, request, obj=None):
        """
        Evitamos el borrado físico de imágenes.
        """

        return False