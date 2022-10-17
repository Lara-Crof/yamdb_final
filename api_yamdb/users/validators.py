from django.core.exceptions import ValidationError


def usernamevalidator(value):
    """Валидация никнейма пользователя на запрещенные значения."""
    if value == 'me':
        raise ValidationError(
            'Имя пользователя не может быть <me>.',
            params={'value': value},
        )
