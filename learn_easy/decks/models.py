from django.db import models
from usersApp.models import CustomUser 
from cards.models import Card


class Deck(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cards = models.ManyToManyField(Card, through='DeckCard')
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.deck.name} - {self.card.word}'
    
    
    