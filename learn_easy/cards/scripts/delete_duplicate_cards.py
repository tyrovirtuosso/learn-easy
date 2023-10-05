from cards.models import Card, Level
from usersApp.models import CustomUser
import os
import django
from pprint import pprint
from django.db.models import Count


# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn_easy.settings")

# Initialize Django
django.setup()

def remove_duplicate_cards():
    # Get all users
    users = CustomUser.objects.all()
    
    for user in users:
        # Get all cards for the current user
        cards = Card.objects.filter(user=user)
        
        # Find duplicate cards
        duplicates = cards.values('card_name').annotate(name_count=Count('card_name')).filter(name_count__gt=1)
        
        for duplicate in duplicates:
            # Get all cards with this name
            dup_cards = cards.filter(card_name=duplicate['card_name'])
            
            # Keep the first one and delete the rest
            first_one = dup_cards.first()
            dup_cards.exclude(id=first_one.id).delete()



def run():
    remove_duplicate_cards()