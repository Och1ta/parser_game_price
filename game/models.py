from django.db import models


class GameName(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название Игры'
    )

    def __str__(self):
        return self.name
