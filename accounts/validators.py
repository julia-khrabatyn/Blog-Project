from datetime import date
from django.core.exceptions import ValidationError


def validate_birth_date(value: date):
    """
    Validate if birth_day value from the past
    and raise ValidationError when it is from the future
    or user is younger that 13 y.o.
    """
    today = date.today()
    if value > today:
        raise ValidationError("Birth date can not be from the future!")

    age = (
        today.year
        - value.year
        - ((today.month, today.day) < (value.month, value.day))
    )
    if age < 13:
        raise ValidationError("Birth date can not be less than 13 y.o. !")
