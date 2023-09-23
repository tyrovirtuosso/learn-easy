# Generated by Django 4.2.5 on 2023-09-23 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("items", "0003_notification"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Deck",
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
                ("name", models.CharField(max_length=255)),
                ("is_public", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="DeckItem",
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
                    "deck",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="decks.deck"
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="items.item"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="deck",
            name="items",
            field=models.ManyToManyField(through="decks.DeckItem", to="items.item"),
        ),
        migrations.AddField(
            model_name="deck",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]