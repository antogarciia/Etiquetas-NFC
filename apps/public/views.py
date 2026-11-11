from django.shortcuts import get_object_or_404
from django.shortcuts import render

from apps.tags.models import Tag
from apps.tags.models import TagStatus


def tag_detail(request, short_code):
    """
    Página pública mostrada al escanear un NFC.
    """

    tag = get_object_or_404(
        Tag.objects.select_related(
            "company",
            "asset",
        ),
        short_code=short_code,
        is_public=True,
        status=TagStatus.ASSIGNED,
        is_active=True,
    )

    tag.increment_scan_counter()

    return render(
        request,
        "public/tag_detail.html",
        {
            "tag": tag,
            "asset": tag.asset,
            "company": tag.company,
        },
    )