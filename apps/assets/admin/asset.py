from django.contrib import admin, messages

from apps.assets.models import Asset
from apps.assets.models.asset import AssetStatus

from apps.assets.admin.tag_inline import TagInline

from .inlines import AssetImageInline

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    inlines = (
        TagInline,
        AssetImageInline,
    )

    # =====================================================
    # GENERAL
    # =====================================================

    list_per_page = 25

    ordering = (
        "name",
    )

    date_hierarchy = "created_at"



    # =====================================================
    # LIST DISPLAY
    # =====================================================

    list_display = (

        "asset_code_display",
        "name",
        "company_name",
        "category_name",
        "status",
        "city",
        "price_display",
        "tag_status",
        "public_asset",
        "featured_asset",
        "active_asset",

    )



    # =====================================================
    # FILTERS
    # =====================================================

    list_filter = (

        "status",
        "category",
        "company",
        "is_public",
        "is_featured",
        "is_active",
        "created_at",

    )



    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (

        "asset_code",
        "name",
        "slug",
        "internal_reference",
        "city",
        "province",
        "company__name",
        "category__name",
        "responsible_user__username",

    )



    # =====================================================
    # AUTOCOMPLETE
    # =====================================================

    autocomplete_fields = (

        "company",
        "category",
        "responsible_user",

    )



    # =====================================================
    # READONLY
    # =====================================================

    readonly_fields = (

        "uuid",
        "asset_code",
        "slug",
        "created_at",
        "updated_at",
        "is_active",

    )



    # =====================================================
    # FIELDSETS
    # =====================================================

    fieldsets = (

        (
            "Información general",
            {
                "fields": (

                    "company",
                    "category",
                    "asset_code",
                    "name",
                    "slug",
                    "internal_reference",

                )
            },
        ),


        (
            "Descripción",
            {
                "fields": (

                    "description",

                )
            },
        ),


        (
            "Localización",
            {
                "fields": (

                    "address",
                    "postal_code",
                    "city",
                    "province",
                    "country",
                    "latitude",
                    "longitude",

                )
            },
        ),


        (
            "Estado",
            {
                "fields": (

                    "status",
                    "is_public",
                    "published_at",
                    "is_featured",
                    "is_active",

                )
            },
        ),


        (
            "Precio",
            {
                "fields": (

                    "price",
                    "currency",
                    "available_from",

                )
            },
        ),


        (
            "Responsable",
            {
                "fields": (

                    "responsible_user",

                )
            },
        ),


        (
            "Identificación",
            {
                "fields": (

                    "uuid",

                )
            },
        ),


        (
            "Fechas",
            {
                "fields": (

                    "created_at",
                    "updated_at",

                )
            },
        ),

    )



    # =====================================================
    # QUERYSET
    # =====================================================

    def get_queryset(self, request):

        queryset = Asset.all_objects.all()

        return queryset.select_related(

            "company",
            "category",
            "responsible_user",

        ).prefetch_related(
            "tag",
        )



    # =====================================================
    # DISPLAY
    # =====================================================


    @admin.display(
        description="Código",
        ordering="asset_code",
    )
    def asset_code_display(self, obj):

        return obj.asset_code



    @admin.display(
        description="Empresa",
    )
    def company_name(self, obj):

        return obj.company.name



    @admin.display(
        description="Categoría",
    )
    def category_name(self, obj):

        return obj.category.name



    @admin.display(
        description="Precio",
    )
    def price_display(self, obj):

        if obj.price:

            return f"{obj.price} {obj.currency}"

        return "-"



    @admin.display(
        description="Tag NFC",
    )
    def tag_status(self, obj):

        if hasattr(obj, "tag"):

            return obj.tag.short_code

        return "-"



    @admin.display(
        description="Público",
        boolean=True,
    )
    def public_asset(self, obj):

        return obj.is_public



    @admin.display(
        description="Destacado",
        boolean=True,
    )
    def featured_asset(self, obj):

        return obj.is_featured



    @admin.display(
        description="Activo",
        boolean=True,
    )
    def active_asset(self, obj):

        return obj.is_active



    # =====================================================
    # ACTIONS
    # =====================================================


    actions = (

        "mark_available",
        "mark_reserved",
        "mark_sold",
        "mark_rented",
        "mark_archived",
        "activate_assets",
        "deactivate_assets",
        "make_public",
        "make_private",
        "make_featured",
        "remove_featured",

    )



    @admin.action(
        description="Marcar disponibles"
    )
    def mark_available(self, request, queryset):

        queryset.update(
            status=AssetStatus.AVAILABLE
        )



    @admin.action(
        description="Marcar reservados"
    )
    def mark_reserved(self, request, queryset):

        queryset.update(
            status=AssetStatus.RESERVED
        )



    @admin.action(
        description="Marcar vendidos"
    )
    def mark_sold(self, request, queryset):

        queryset.update(
            status=AssetStatus.SOLD
        )



    @admin.action(
        description="Marcar alquilados"
    )
    def mark_rented(self, request, queryset):

        queryset.update(
            status=AssetStatus.RENTED
        )



    @admin.action(
        description="Archivar activos"
    )
    def mark_archived(self, request, queryset):

        for asset in queryset:

            asset.archive()



    @admin.action(
        description="Activar activos"
    )
    def activate_assets(self, request, queryset):

        for asset in queryset:

            asset.activate()



    @admin.action(
        description="Desactivar activos"
    )
    def deactivate_assets(self, request, queryset):

        for asset in queryset:

            asset.soft_delete()



    @admin.action(
        description="Hacer públicos"
    )
    def make_public(self, request, queryset):

        queryset.update(
            is_public=True
        )



    @admin.action(
        description="Hacer privados"
    )
    def make_private(self, request, queryset):

        queryset.update(
            is_public=False
        )



    @admin.action(
        description="Marcar destacados"
    )
    def make_featured(self, request, queryset):

        queryset.update(
            is_featured=True
        )



    @admin.action(
        description="Quitar destacados"
    )
    def remove_featured(self, request, queryset):

        queryset.update(
            is_featured=False
        )



    # =====================================================
    # PERMISOS
    # =====================================================


    def has_delete_permission(
        self,
        request,
        obj=None
    ):

        return False



    def get_readonly_fields(
        self,
        request,
        obj=None
    ):

        readonly = list(
            self.readonly_fields
        )


        if obj is not None:

            readonly.extend(
                [
                    "company",
                    "asset_code",
                ]
            )


        return readonly