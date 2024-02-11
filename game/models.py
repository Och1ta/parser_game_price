from django.db import models


class GameName(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название Игры'
    )

    def __str__(self):
        return self.name


class GameUrl(models.Model):
    url = models.TextField(
        max_length=300,
        verbose_name='Ссылка на игру'
    )


class Game(models.Model):
    name = models.ManyToManyField(
        GameName,
        verbose_name='Название игры'
    )
    url = models.ManyToManyField(
        GameUrl,
        verbose_name='Ссылка на игры'
    )
