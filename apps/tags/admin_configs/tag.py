from django.contrib import admin

from apps.tags.models import Tag
from apps.tags.models.tag import TagStatus


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    # -------------------------------------------------
    # GENERAL
    # -------------------------------------------------

    list_per_page = 25

    ordering = (
        "short_code",
    )

    date_hierarchy = "created_at"


    # -------------------------------------------------
    # LIST
    # -------------------------------------------------

    list_display = (
        "tag_code",
        "company_name",
        "asset_name",
        "status",
        "tag_type",
        "scans",
        "public_tag",
        "active_tag",
        "last_scan_at",
    )


    # -------------------------------------------------
    # FILTERS
    # -------------------------------------------------

    list_filter = (
        "status",
        "tag_type",
        "is_public",
        "is_active",
        "company",
        "created_at",
    )


    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    search_fields = (
        "short_code",
        "uuid",
        "company__name",
        "asset__name",
    )


    # -------------------------------------------------
    # AUTOCOMPLETE
    # -------------------------------------------------

    autocomplete_fields = (
        "company",
        "asset",
    )


    # -------------------------------------------------
    # READONLY
    # -------------------------------------------------

    readonly_fields = (
        "uuid",
        "scan_count",
        "last_scan_at",
        "activated_at",
        "deactivated_at",
        "created_at",
        "updated_at",
        "is_active",
    )


    # -------------------------------------------------
    # FIELDSETS
    # -------------------------------------------------

    fieldsets = (

        (
            "Información general",
            {
                "fields": (
                    "company",
                    "asset",
                    "uuid",
                ),
            },
        ),


        (
            "Configuración",
            {
                "fields": (
                    "status",
                    "tag_type",
                    "is_public",
                    "is_active",
                ),
            },
        ),


        (
            "Estadísticas",
            {
                "fields": (
                    "scan_count",
                    "last_scan_at",
                ),
            },
        ),


        (
            "Notas",
            {
                "fields": (
                    "notes",
                ),
            },
        ),


        (
            "Fechas",
            {
                "fields": (
                    "activated_at",
                    "deactivated_at",
                    "created_at",
                    "updated_at",
                ),
            },
        ),

    )


    # -------------------------------------------------
    # QUERYSET
    # -------------------------------------------------

    def get_queryset(self, request):

        queryset = Tag.all_objects.all()

        return queryset.select_related(
            "company",
            "asset",
        )


    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------

    @admin.display(
        description="Código",
        ordering="short_code",
    )
    def tag_code(self, obj):

        return obj.short_code


    @admin.display(
        description="Empresa",
        ordering="company",
    )
    def company_name(self, obj):

        return obj.company.name


    @admin.display(
        description="Activo asociado",
    )
    def asset_name(self, obj):

        if obj.asset:
            return obj.asset.name

        return "-"


    @admin.display(
        description="Escaneos",
        ordering="scan_count",
    )
    def scans(self, obj):

        return obj.scan_count


    @admin.display(
        description="Pública",
        boolean=True,
    )
    def public_tag(self, obj):

        return obj.is_public


    @admin.display(
        description="Activo",
        boolean=True,
        ordering="is_active",
    )
    def active_tag(self, obj):

        return obj.is_active



    # -------------------------------------------------
    # ACTIONS
    # -------------------------------------------------

    actions = (
        "mark_available",
        "mark_blocked",
        "mark_archived",
        "make_public",
        "make_private",
        "deactivate_tags",
        "activate_tags",
    )


    @admin.action(
        description="Marcar como disponibles"
    )
    def mark_available(self, request, queryset):

        queryset.update(
            status=TagStatus.AVAILABLE,
            deactivated_at=None,
        )


    @admin.action(
        description="Marcar como bloqueadas"
    )
    def mark_blocked(self, request, queryset):

        queryset.update(
            status=TagStatus.BLOCKED,
        )


    @admin.action(
        description="Marcar como archivadas"
    )
    def mark_archived(self, request, queryset):

        queryset.update(
            status=TagStatus.ARCHIVED,
        )


    @admin.action(
        description="Hacer públicas"
    )
    def make_public(self, request, queryset):

        queryset.update(
            is_public=True,
        )


    @admin.action(
        description="Hacer privadas"
    )
    def make_private(self, request, queryset):

        queryset.update(
            is_public=False,
        )


    @admin.action(
        description="Desactivar etiquetas seleccionadas"
    )
    def deactivate_tags(self, request, queryset):

        for tag in queryset:
            tag.soft_delete()


    @admin.action(
        description="Activar etiquetas seleccionadas"
    )
    def activate_tags(self, request, queryset):

        for tag in queryset:
            tag.activate()



    # -------------------------------------------------
    # PERMISOS
    # -------------------------------------------------

    def has_delete_permission(self, request, obj=None):
        """
        Evitamos eliminar etiquetas desde el admin.
        Se recomienda archivarlas para mantener el historial.
        """

        return False


    def get_readonly_fields(self, request, obj=None):

        readonly = list(self.readonly_fields)

        if obj is not None:
            readonly.extend(
                [
                    "company",
                    "short_code",
                ]
            )

        return readonly