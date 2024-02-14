from django.db import models


class Game(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название игры'
    )
    price = models.CharField(
        max_length=100,
        verbose_name='Цена на игру'
    )
    url = models.CharField(
        max_length=300,
        verbose_name='Ссылка на игру'
    )
