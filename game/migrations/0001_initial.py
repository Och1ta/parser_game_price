# Generated by Django 5.0.2 on 2024-02-18 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название игры')),
                ('price', models.CharField(max_length=100, verbose_name='Цена на игру')),
                ('url', models.CharField(max_length=300, verbose_name='Ссылка на игру')),
            ],
        ),
    ]
