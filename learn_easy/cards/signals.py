from django.db.models.signals import post_save, pre_save, post_migrate
from django.dispatch import receiver
from .models import Card, Level
from .scripts.add_levels import add_levels

from decks.models import Deck, DeckCard

@receiver(post_save, sender=Card)
def create_default_deck_for_new_card(sender, instance, created, **kwargs):
    if created:
        # Check if the user already has a "default" deck
        default_deck, created = Deck.objects.get_or_create(
            user=instance.user,
            name="Default",
        )
        # Check if the card is already in the default deck
        if not DeckCard.objects.filter(deck=default_deck, card=instance).exists():
            # Add the card to the default deck
            DeckCard.objects.create(deck=default_deck, card=instance)

@receiver(pre_save, sender=Card)
def set_default_level(sender, instance, **kwargs):
    if instance.level_id is None:
        # Get the Level instance with level_number equal to 1
        level_one = Level.objects.get(level_number=1)
        instance.level = level_one


@receiver(post_migrate)
def create_levels(sender, **kwargs):
    add_levels()