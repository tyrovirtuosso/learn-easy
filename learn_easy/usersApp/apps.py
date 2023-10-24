from django.apps import AppConfig

class UsersAppConfig(AppConfig):
    """
    Configuration class for the UsersApp in Django.

    This class defines configuration settings for the UsersApp, including the
    default_auto_field and a human-readable verbose_name.

    Attributes:
        default_auto_field (str): The name of the default AutoField for models.
        name (str): The name of the app.
        verbose_name (str): A human-readable name for the app.
    """
    
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'usersApp'
    verbose_name: str = 'App for managing the Users table and authentication'

