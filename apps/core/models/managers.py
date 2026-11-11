from django.db import models


class ActiveManager(models.Manager):
    """
    Devuelve únicamente los registros activos.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AllObjectsManager(models.Manager):
    """
    Devuelve todos los registros.
    """

    def get_queryset(self):
        return super().get_queryset()