from django.contrib import admin
from django.db.models import Count
from django.core.exceptions import ValidationError

from .models import Company, CompanyMembership
from .models.membership import ROLE_CHOICES


# ==================================================
# INLINE MEMBERSHIP
# ==================================================

class CompanyMembershipInline(admin.TabularInline):

    model = CompanyMembership

    extra = 0

    can_delete = False

    autocomplete_fields = (
        "user",
    )

    fields = (
        "user",
        "role",
        "is_active",
    )

    readonly_fields = (
        "role",
    )


# ==================================================
# COMPANY ADMIN
# ==================================================

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_per_page = 25

    ordering = (
        "name",
    )

    autocomplete_fields = (
        "owner",
    )

    list_display = (
        "name",
        "owner",
        "industry",
        "city",
        "is_active",
        "members_count",
        "created_at",
    )

    list_filter = (
        "industry",
        "is_active",
        "country",
        "owner",
    )

    search_fields = (
        "name",
        "email",
        "city",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    inlines = [
        CompanyMembershipInline,
    ]


    fieldsets = (

        (
            "Información general",
            {
                "fields": (
                    "owner",
                    "name",
                    "slug",
                    "industry",
                    "logo",
                    "description",
                ),
            },
        ),


        (
            "Contacto",
            {
                "fields": (
                    "email",
                    "phone",
                    "website",
                ),
            },
        ),


        (
            "Ubicación",
            {
                "fields": (
                    "address",
                    "city",
                    "country",
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


    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        return queryset.annotate(
            total_members=Count(
                "memberships"
            )
        )


    @admin.display(
        description="Miembros",
        ordering="total_members",
    )
    def members_count(self, obj):

        return obj.total_members



# ==================================================
# COMPANY MEMBERSHIP ADMIN
# ==================================================

@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):

    list_per_page = 25

    ordering = (
        "company",
        "role",
    )


    list_display = (
        "user",
        "company",
        "role",
        "is_active",
        "created_at",
    )


    list_filter = (
        "role",
        "is_active",
        "company",
    )


    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "company__name",
        "company__owner__email",
    )


    readonly_fields = (
        "created_at",
        "updated_at",
    )


    autocomplete_fields = (
        "user",
        "company",
    )


    date_hierarchy = "created_at"


    fieldsets = (

        (
            "Relación",
            {
                "fields": (
                    "user",
                    "company",
                ),
            },
        ),


        (
            "Permisos",
            {
                "fields": (
                    "role",
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
        "activate_members",
        "deactivate_members",
    ]


    # ----------------------------------------------
    # Protección del Owner
    # ----------------------------------------------

    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):

        if change:

            old_membership = CompanyMembership.objects.get(
                pk=obj.pk
            )


            # No permitir cambiar el rol del owner

            if (
                old_membership.role == ROLE_CHOICES.OWNER
                and obj.role != ROLE_CHOICES.OWNER
            ):

                raise ValidationError(
                    "No se puede modificar el rol del propietario de la empresa."
                )


            # No permitir desactivar el único owner

            if (
                old_membership.role == ROLE_CHOICES.OWNER
                and old_membership.is_active
                and not obj.is_active
            ):

                remaining_owner = CompanyMembership.objects.filter(
                    company=obj.company,
                    role=ROLE_CHOICES.OWNER,
                    is_active=True,
                ).exclude(
                    pk=obj.pk,
                ).exists()


                if not remaining_owner:

                    raise ValidationError(
                        "No se puede desactivar el único propietario activo de la empresa."
                    )


        super().save_model(
            request,
            obj,
            form,
            change,
        )


    # ----------------------------------------------
    # Acciones masivas
    # ----------------------------------------------

    @admin.action(
        description="Activar miembros seleccionados"
    )
    def activate_members(
        self,
        request,
        queryset,
    ):

        queryset.update(
            is_active=True,
        )


    @admin.action(
        description="Desactivar miembros seleccionados"
    )
    def deactivate_members(
        self,
        request,
        queryset,
    ):

        queryset.update(
            is_active=False,
        )