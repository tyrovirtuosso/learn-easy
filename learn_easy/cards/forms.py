from django import forms
from .models import Card
from decks.models import Deck
from django.db import transaction

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name', 'decks']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CardForm, self).__init__(*args, **kwargs)
        
        # Customize the labels if needed
        # self.fields['card_name'].label = "Card Name"
        # self.fields['new_deck_name'].label = "New Deck Name"

    def save(self, commit=True):
        card = super().save(commit=False)
        card.user = self.user
        if commit:
            with transaction.atomic():
                card.save()
                selected_decks = self.cleaned_data.get('decks')
                if not selected_decks:
                    selected_decks = [Deck.objects.get(name='default', user=self.user)]
                for deck in selected_decks:
                    card.decks.add(deck)
        return card
    
        
    # def clean(self):
    #     cleaned_data = super().clean()
    #     card_name = cleaned_data.get('card_name')
    #     new_deck_name = cleaned_data.get('new_deck_name')

    #     # Check if no decks are selected, and 'Default' is chosen
    #     if not cleaned_data.get('decks'):
    #         default_deck, created = Deck.objects.get_or_create(user=self.user, name='Default')
    #         cleaned_data['decks'] = [default_deck]

    #     # Check if a new deck name is provided and create it
    #     if new_deck_name:
    #         # Ensure that deck names are case-insensitive unique
    #         new_deck_name_lower = new_deck_name.lower()
    #         new_deck, created = Deck.objects.get_or_create(
    #             user=cleaned_data['user'],
    #             name=new_deck_name_lower,
    #         )
    #         cleaned_data['decks'].append(new_deck)

    #     return cleaned_data
