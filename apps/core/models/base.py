import uuid

from django.db import models

from .managers import ActiveManager, AllObjectsManager


class BaseModel(models.Model):
    """
    Modelo base para toda la plataforma.
    """

    id = models.BigAutoField(
        primary_key=True
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        default=True
    )

    objects = ActiveManager()

    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        """
        Desactiva el registro sin eliminarlo físicamente.
        """
        self.is_active = False
        self.save(update_fields=["is_active"])

    def restore(self):
        """
        Reactiva un registro.
        """
        self.is_active = True
        self.save(update_fields=["is_active"])