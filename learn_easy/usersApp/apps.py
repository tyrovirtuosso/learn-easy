from django.apps import AppConfig

# INSTALLED_APPS may contain the dotted path to a configuration class to specify it explicitly
class UsersappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usersApp"
    verbose_name = "App for managing the Users table and authentication"
