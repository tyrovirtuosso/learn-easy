from django.apps import AppConfig


class DecksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "decks"
    verbose_name = "App for managing the Decks table"