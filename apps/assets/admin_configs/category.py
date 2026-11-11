from django.contrib import admin

from ..models import AssetCategory


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):

    list_per_page = 25

    ordering = (
        "display_order",
        "name",
    )

    list_display = (
        "name",
        "company",
        "icon_name",
        "color",
        "display_order",
        "is_active",
        "created_at",
    )

    list_filter = (
        "company",
        "icon_name",
        "is_active",
    )

    search_fields = (
        "name",
        "slug",
        "company__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "company",
    )

    date_hierarchy = "created_at"


    fieldsets = (

        (
            "Información general",
            {
                "fields": (
                    "company",
                    "name",
                    "slug",
                    "description",
                ),
            },
        ),

        (
            "Diseño",
            {
                "fields": (
                    "color",
                    "icon_name",
                    "display_order",
                ),
            },
        ),

        (
            "Estado",
            {
                "fields": (
                    "is_active",
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
        "activate_categories",
        "deactivate_categories",
    ]


    @admin.action(
        description="Activar categorías seleccionadas"
    )
    def activate_categories(self, request, queryset):

        queryset.update(
            is_active=True,
        )


    @admin.action(
        description="Desactivar categorías seleccionadas"
    )
    def deactivate_categories(self, request, queryset):

        queryset.update(
            is_active=False,
        )