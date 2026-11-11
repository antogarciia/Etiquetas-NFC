import uuid

from django.db import models

from .managers import ActiveManager, AllObjectsManager


class BaseModel(models.Model):
    """
    Modelo base para todas las entidades de la plataforma.
    """

    id = models.BigAutoField(
        primary_key=True,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    objects = ActiveManager()

    all_objects = AllObjectsManager()


    class Meta:

        abstract = True

        ordering = [
            "-created_at",
        ]


    # =====================================
    # SOFT DELETE
    # =====================================

    def soft_delete(self):

        self.is_active = False

        self.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )


    def activate(self):

        self.is_active = True

        self.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )


    def hard_delete(self):

        super().delete()


    # =====================================
    # REPRESENTATION
    # =====================================

    def __str__(self):

        return f"{self.__class__.__name__} ({self.uuid})"