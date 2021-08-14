from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_phone(value):
    if value.isdigit():
        RegexValidator(regex=r'^\+?1?\d{9,15}$',
                       message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return value
    else:
        raise ValidationError(" please enter valid phone")
