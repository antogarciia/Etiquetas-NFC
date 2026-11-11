"""
Validadores reutilizables del proyecto.
"""

from django.core.validators import RegexValidator


slug_validator = RegexValidator(
    regex=r"^[a-z0-9-]+$",
    message="Solo se permiten letras minúsculas, números y guiones.",
)

hex_color_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="El color debe estar en formato hexadecimal (#RRGGBB).",
)

phone_validator = RegexValidator(
    regex=r"^[0-9+\-\s()]+$",
    message="Introduce un número de teléfono válido.",
)