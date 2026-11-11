from django.contrib import admin

from apps.assets.models import AssetCategory


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):

    # -------------------------------------------------
    # GENERAL
    # -------------------------------------------------

    list_per_page = 25

    ordering = (
        "name",
    )


    # -------------------------------------------------
    # LIST
    # -------------------------------------------------

    list_display = (
        "name",
        "company_name",
        "icon_name",
        "color",
        "display_order",
        "active_category",
    )


    # -------------------------------------------------
    # FILTERS
    # -------------------------------------------------

    list_filter = (
        "company",
        "icon_name",
        "is_active",
    )


    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    search_fields = (
        "name",
        "slug",
        "company__name",
    )


    # -------------------------------------------------
    # AUTOCOMPLETE
    # -------------------------------------------------

    search_fields = (
        "name",
        "slug",
        "company__name",
    )


    # -------------------------------------------------
    # READONLY
    # -------------------------------------------------

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
        "uuid",
    )


    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------

    @admin.display(
        description="Empresa",
        ordering="company",
    )
    def company_name(self, obj):

        return obj.company.name



    @admin.display(
        description="Activo",
        boolean=True,
        ordering="is_active",
    )
    def active_category(self, obj):

        return obj.is_active