from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import usernamevalidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    """Кастомная модель пользователя"""
    username = models.CharField(
        verbose_name='Ник пользователя',
        validators=(usernamevalidator,),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Почта пользователя',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=20,
        choices=ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(
        verbose_name='Код пользователя',
        max_length=30,
        null=True,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
