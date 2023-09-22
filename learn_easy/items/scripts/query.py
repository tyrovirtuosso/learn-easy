from items.models import Item
from usersApp.models import CustomUser
import os
import django
from pprint import pprint


# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn_easy.settings")

# Initialize Django
django.setup()


def getAllItemsWithFieldValues(model):
    items = model.objects.all()
    for item in items:    
        print()
        for field in model._meta.fields:
            field_name = field.name
            field_value = getattr(item, field_name)
            print(f"{item}.{field_name}: {field_value}")

def run():
    getAllItemsWithFieldValues(CustomUser)