from django.db import models
from usersApp.models import CustomUser 
from items.models import Item


class Deck(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    items = models.ManyToManyField(Item, through='DeckItem')
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class DeckItem(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.deck.name} - {self.item.word}'
    
    
    