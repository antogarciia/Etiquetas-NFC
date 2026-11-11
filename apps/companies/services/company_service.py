from django.db import transaction

from apps.accounts.models import User

from apps.companies.models import (
    Company,
    CompanyMembership,
)

class CompanyService:

    @staticmethod
    @transaction.atomic
    def create_company(
        owner: User,
        **company_data,
    ):

        company = Company.objects.create(
            **company_data,
        )

        CompanyMembership.objects.create(
            user=owner,
            company=company,
            role="owner",
        )

        return company
    
    @staticmethod
    @transaction.atomic
    def add_member(
        company: Company,
        user: User,
        role: str,
    ):

        if CompanyMembership.objects.filter(
            company=company,
            user=user,
        ).exists():

            raise ValueError(
                "El usuario ya pertenece a esta empresa."
            )

        membership = CompanyMembership.objects.create(
            company=company,
            user=user,
            role=role,
        )

        return membership
    
    
    
