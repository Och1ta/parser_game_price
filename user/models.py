from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

from constans import MAX_LEN_EMAIL, MAX_LEN_NAME
from user.validators import username_validator


class User(AbstractUser):
    """Кастомная модель User."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username', 'password',
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=MAX_LEN_EMAIL,
        unique=True,
        validators=[EmailValidator],
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_LEN_NAME,
        unique=True,
        validators=(username_validator,),
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return '{} {}'.format(self.username, self.email)
