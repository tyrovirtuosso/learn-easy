from cards.models import Card, Level
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
            
def delete_all(model):
    values = model.objects.all()
    count = values.count()
    values.delete()
    print(f'Deleted {count} items.')

def run():
    delete_all(Level)