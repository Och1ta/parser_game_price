from django.db import models

from user.models import User


class Game(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название игры'
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Старая цена',
        null=True,
        blank=True
    )
    new_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Новая цена',
        null=True,
        blank=True
    )
    url = models.CharField(
        max_length=300,
        verbose_name='Ссылка на игру'
    )

    def __str__(self):
        return self.name


class FavoriteGame(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='Любимая игра'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.game.name}"
