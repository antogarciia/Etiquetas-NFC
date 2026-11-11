from apps.common.permissions import CompanyPermissions


class CompanyAccessService:
    """
    Servicio encargado de resolver permisos
    de un usuario dentro de una empresa.
    """


    def __init__(self, membership):

        self.membership = membership

        self.permissions = CompanyPermissions(
            membership
        )


    def can_access_company(self):

        return self.membership.is_active


    def can_manage_company(self):

        return self.permissions.can_manage_company()


    def can_manage_members(self):

        return self.permissions.can_manage_members()


    def can_change_roles(self):

        return self.permissions.can_change_roles()


    def can_manage_assets(self):

        return self.permissions.can_manage_assets()


    def can_delete_assets(self):

        return self.permissions.can_delete_assets()


    def can_publish_assets(self):

        return self.permissions.can_publish_assets()


    def can_view(self):

        return self.permissions.can_view()