from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Card
from decks.models import Deck, DeckCard

@receiver(post_save, sender=Card)
def create_default_deck(sender, instance, created, **kwargs):
    if created:
        # Check if the user already has a "default" deck
        default_deck, created = Deck.objects.get_or_create(
            user=instance.user,
            name="default",
        )
        # Add the card to the default deck
        DeckCard.objects.create(deck=default_deck, card=instance)