from django.db import models
import datetime
from django.utils import timezone

class Deck(models.Model):
    user = models.ForeignKey('usersApp.CustomUser', on_delete=models.CASCADE)
    deck_name = models.CharField(max_length=255, verbose_name="Deck Name")
    is_public = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'deck_name']
    
    def get_cards_for_revision(self):
        # Get the current date
        today = timezone.now()
        # Get the cards in this deck that are due for review
        cards_due_for_review = self.cards.filter(review__next_review__lte=today)
        cards_due_for_review = self.cards.filter(review__next_review__lte=today).order_by('-review__next_review')
        return cards_due_for_review

    def __str__(self):
        return self.deck_name
    
    def save(self, *args, **kwargs):
        self.deck_name = self.deck_name.lower()
        super(Deck, self).save(*args, **kwargs)


class SmartDeck(models.Model):
    user = models.ForeignKey('usersApp.CustomUser', on_delete=models.CASCADE)
    smart_deck_name = models.CharField(max_length=255, verbose_name="Smart Deck Name")
    is_public = models.BooleanField(default=False)
    smart_deck_tags = models.ManyToManyField('cards.Tag', related_name="smart_deck_tags", verbose_name="Smart Decks Tags")

    class Meta:
        unique_together = ['user', 'smart_deck_name']
    
    def __str__(self):
        return self.deck_name
    
    def save(self, *args, **kwargs):
        self.deck_name = self.deck_name.lower()
        super(Deck, self).save(*args, **kwargs)