class CompanyPermissions:
    """
    Capa centralizada de permisos de empresa.

    Recibe una instancia de CompanyMembership
    y decide qué acciones puede realizar.
    """


    def __init__(self, membership):

        self.membership = membership


    # -------------------------
    # Empresa
    # -------------------------

    def can_manage_company(self):

        return self.membership.can_manage_company()


    def can_delete_company(self):

        return self.membership.can_delete_company()


    # -------------------------
    # Usuarios
    # -------------------------

    def can_manage_members(self):

        return self.membership.can_manage_members()


    def can_change_roles(self):

        return self.membership.can_change_roles()


    # -------------------------
    # Activos
    # -------------------------

    def can_manage_assets(self):

        return self.membership.can_manage_assets()


    def can_delete_assets(self):

        return self.membership.can_delete_assets()


    def can_publish_assets(self):

        return self.membership.can_publish_assets()


    # -------------------------
    # Lectura
    # -------------------------

    def can_view(self):

        return self.membership.can_view()