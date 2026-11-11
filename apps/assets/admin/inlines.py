from django.contrib import admin
from django.utils.html import format_html

from apps.assets.models import AssetImage


class AssetImageInline(admin.TabularInline):

    model = AssetImage

    extra = 1

    fields = (

        "preview",

        "image",

        "title",

        "display_order",

        "is_cover",

        "is_active",

    )

    readonly_fields = (

        "preview",

    )

    ordering = (

        "display_order",

    )


    @admin.display(description="Vista previa")
    def preview(self, obj):

        if obj.pk and obj.image:

            return format_html(
                '<img src="{}" '
                'style="height:70px;'
                'width:100px;'
                'object-fit:cover;'
                'border-radius:8px;" />',
                obj.image.url,
            )

        return "-"