from django.db.models.signals import post_save, pre_save, post_migrate
from django.dispatch import receiver
from .scripts.add_levels import add_levels
from django.utils import timezone

from decks.models import Deck
from cards.models import Card, Level, Review
from usersApp.models import CustomUser
from .tasks import update_card_meaning, update_card_tags


@receiver(post_migrate)
def create_levels(sender, **kwargs):
    add_levels()

@receiver(post_save, sender=CustomUser)
def create_default_deck(sender, instance, created, **kwargs):
    if created:
        Deck.objects.create(deck_name='default', user=instance)
        
@receiver(post_save, sender=Card)
def create(sender, instance, created, **kwargs):
    if created:
        update_card_meaning.delay(instance.pk)
        update_card_tags.delay(instance.pk)
        

@receiver(post_save, sender=Card)
def create_review(sender, instance, created, **kwargs):
    if created:
        Review.objects.create(
            card=instance, 
            next_review=timezone.now(),
            level= Level.objects.get(level_number=1)
        )
        
