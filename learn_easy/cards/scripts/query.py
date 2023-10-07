from cards.models import Card, Level, Tag
from usersApp.models import CustomUser
import os
import django
from pprint import pprint
from django.db.models import Count, F, Value
from django.db.models.functions import Concat
import pandas as pd
from openai_API.api import OpenAI_API

ai = OpenAI_API()


# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn_easy.settings")

# Initialize Django
django.setup()

def get_tags():
    unique_tags = Tag.objects.values('id', 'tag_name').distinct()
    tag_list = list(unique_tags)
    print("generating organized tags")
    organized_tags = ai.organize_tags(tag_list)
    print(organized_tags)
    # print(tag_list)    
    # for tag in tag_list:
    #     print(tag)


def get_all_tags_card_association():
    # Query to retrieve unique tag names and associated system_defined_cards
    unique_tags_and_system_cards = Tag.objects.filter(
        system_defined_cards__isnull=False  # Filter tags with system_defined_cards
    ).annotate(
        card_count=Count('system_defined_cards')
    ).filter(
        card_count__gt=0
    )

    # Create a list to store tuples of (tag_name, card_names)
    tag_card_list = []

    # Iterate through the query results and populate the list
    for tag in unique_tags_and_system_cards:
        tag_name = tag.tag_name
        card_names = list(tag.system_defined_cards.values_list('card_name', flat=True))
        tag_card_list.append((tag_name, card_names))
        

    # Sort the list based on the number of card_names (card_count)
    tag_card_list_sorted = sorted(tag_card_list, key=lambda x: len(x[1]), reverse=True)
    
    data = [{'Tag Name': tag_name, 'Card Names': ', '.join(card_names)} for tag_name, card_names in tag_card_list_sorted]
    
    # Printing the sorted results
    for tag_name, card_names in tag_card_list_sorted:
        # card_names_str = ', '.join(card_names)
        # print(f"Tag Name: {tag_name}, Card Names: {card_names_str}")
        print(tag_name)
        print(card_names)
        print()
        
def getAllCardNames():
    unique_card_names = list(Card.objects.values_list('card_name', flat=True).distinct())
    print(unique_card_names)
    

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
    getAllCardNames()
    # delete_all(Level)