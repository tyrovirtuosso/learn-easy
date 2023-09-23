from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item
from decks.models import Deck, DeckItem

@receiver(post_save, sender=Item)
def create_default_deck(sender, instance, created, **kwargs):
    if created:
        # Check if the user already has a "default" deck
        default_deck, created = Deck.objects.get_or_create(
            user=instance.user,
            name="default",
        )
        # Add the item to the default deck
        DeckItem.objects.create(deck=default_deck, item=instance)
