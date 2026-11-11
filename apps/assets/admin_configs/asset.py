from django.contrib import admin
from django.db.models import Count

from ..models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_per_page = 25

    ordering = (
        "name",
    )

    list_display = (
        "name",
        "company",
        "category",
        "status",
        "city",
        "responsible_user",
        "is_public",
        "created_at",
    )

    list_filter = (
        "company",
        "category",
        "status",
        "is_public",
        "is_featured",
        "country",
        "city",
    )

    search_fields = (
        "name",
        "slug",
        "internal_reference",
        "company__name",
        "category__name",
        "responsible_user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "published_at",
    )

    autocomplete_fields = (
        "company",
        "category",
        "responsible_user",
    )

    date_hierarchy = "created_at"


    fieldsets = (

        (
            "Información general",
            {
                "fields": (
                    "company",
                    "category",
                    "name",
                    "slug",
                    "internal_reference",
                    "description",
                ),
            },
        ),

        (
            "Ubicación",
            {
                "fields": (
                    "address",
                    "postal_code",
                    "city",
                    "province",
                    "country",
                    "latitude",
                    "longitude",
                ),
            },
        ),

        (
            "Estado y responsable",
            {
                "fields": (
                    "status",
                    "responsible_user",
                ),
            },
        ),

        (
            "Publicación",
            {
                "fields": (
                    "is_public",
                    "is_featured",
                    "published_at",
                ),
            },
        ),

        (
            "Precio",
            {
                "fields": (
                    "price",
                    "currency",
                    "available_from",
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


    actions = [
        "activate_assets",
        "deactivate_assets",
        "publish_assets",
        "unpublish_assets",
    ]


    @admin.action(
        description="Activar activos seleccionados"
    )
    def activate_assets(self, request, queryset):

        queryset.update(
            is_public=True,
        )


    @admin.action(
        description="Desactivar activos seleccionados"
    )
    def deactivate_assets(self, request, queryset):

        queryset.update(
            is_public=False,
        )


    @admin.action(
        description="Publicar activos seleccionados"
    )
    def publish_assets(self, request, queryset):

        queryset.update(
            is_public=True,
        )


    @admin.action(
        description="Ocultar activos seleccionados"
    )
    def unpublish_assets(self, request, queryset):

        queryset.update(
            is_public=False,
        )