from django.core.exceptions import ValidationError


def not_published(value):
    if value:
        raise ValidationError(f'Значение поля is_published при создании объявления не может быть True.')
