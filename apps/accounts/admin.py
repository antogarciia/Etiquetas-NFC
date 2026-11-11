from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_per_page = 25

    ordering = (
        "email",
    )

    readonly_fields = (
        "last_login",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_verified",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "is_verified",
        "language",
        "timezone",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = (

        (
            "Información personal",
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "profile_image",
                )
            },
        ),

        (
            "Configuración",
            {
                "fields": (
                    "language",
                    "timezone",
                    "is_verified",
                )
            },
        ),

        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),

        (
            "Fechas",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = (

        (
            None,
            {
                "classes": (
                    "wide",
                ),

                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )