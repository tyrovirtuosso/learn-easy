from django.db.models.signals import post_save, pre_save, post_migrate
from django.dispatch import receiver
from .scripts.add_levels import add_levels

from decks.models import Deck
from cards.models import Card, Level
from usersApp.models import CustomUser

@receiver(pre_save, sender=Card)
def set_default_level(sender, instance, **kwargs):
    if instance.level_id is None:
        # Get the Level instance with level_number equal to 1
        level_one = Level.objects.get(level_number=1)
        instance.level = level_one

@receiver(post_migrate)
def create_levels(sender, **kwargs):
    add_levels()

@receiver(post_save, sender=CustomUser)
def create_default_deck(sender, instance, created, **kwargs):
    if created:
        Deck.objects.create(deck_name='default', user=instance)