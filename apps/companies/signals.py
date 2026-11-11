from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Company
from .models.membership import CompanyMembership, ROLE_CHOICES

@receiver(post_save, sender=Company)
def create_company_owner_membership(
    sender,
    instance,
    created,
    **kwargs
):

    if not created:
        return


    CompanyMembership.objects.create(
        company=instance,
        user=instance.owner,
        role=ROLE_CHOICES.OWNER,
        is_active=True,
    )