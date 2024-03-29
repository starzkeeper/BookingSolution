# Generated by Django 5.0.3 on 2024-03-28 10:49

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        max_length=4, unique=True, verbose_name="Номер"
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="Цена"
                    ),
                ),
                ("places", models.PositiveSmallIntegerField(max_length=2)),
                ("is_booked", models.BooleanField()),
            ],
            options={
                "verbose_name": "Комнаты",
            },
        ),
    ]
