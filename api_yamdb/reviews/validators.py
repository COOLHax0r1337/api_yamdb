from django.utils import timezone

from django.core.validators import MaxValueValidator


def max_value_current_year(value):
    return MaxValueValidator(
        timezone.now().year, "Год не может быть больше текущего"
    )(value)
