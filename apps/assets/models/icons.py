from django.db import models


class CategoryIcon(models.TextChoices):
    HOUSE = "house", "Casa"
    BUILDING = "building", "Edificio"
    APARTMENT = "apartment", "Apartamento"
    OFFICE = "office", "Oficina"
    WAREHOUSE = "warehouse", "Almacén"
    GARAGE = "garage", "Garaje"
    HOTEL = "hotel", "Hotel"
    RESTAURANT = "restaurant", "Restaurante"
    SHOP = "shop", "Comercio"
    OTHER = "other", "Otro"