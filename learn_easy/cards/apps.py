from django.apps import AppConfig


class CardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cards"
    verbose_name = "App for managing the Cards table"
    
    def ready(self):
        import cards.signals 