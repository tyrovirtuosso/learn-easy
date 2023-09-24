from cards.models import Card
from usersApp.models import CustomUser
import os
import django
from pprint import pprint


# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn_easy.settings")

# Initialize Django
django.setup()


def getAllCardsWithFieldValues(model):
    cards = model.objects.all()
    for card in cards:    
        print()
        for field in model._meta.fields:
            field_name = field.name
            field_value = getattr(card, field_name)
            print(f"{card}.{field_name}: {field_value}")

def run():
    getAllCardsWithFieldValues(CustomUser)