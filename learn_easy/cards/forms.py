from django import forms
from .models import Card
from decks.models import Deck
from django.db import transaction


class CardForm(forms.ModelForm):
    new_deck = forms.CharField(required=False, max_length=255)
    decks = forms.ModelMultipleChoiceField(queryset=Deck.objects.none(), required=False)
    
    class Meta:
        model = Card
        fields = ['card_name', 'decks', 'new_deck']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CardForm, self).__init__(*args, **kwargs)
        
        # Get all decks for the user excluding the 'default' deck
        decks = Deck.objects.filter(user=self.user).exclude(name='default')
        
        if decks.count() > 0:
            # If there are more than one deck, include the 'decks' field
            self.fields['decks'].queryset = decks
        else:
            # If there is only one deck (the 'default' deck), exclude the 'decks' field
            del self.fields['decks']
            self.default_deck_message = "Since there are no custom decks, the card will go to the 'default' deck."
    
    def clean_new_deck(self):
        new_deck_name = self.cleaned_data.get('new_deck')
        
        # If the user typed in a new deck name
        if new_deck_name:
            new_deck_name = new_deck_name.lower()
            if Deck.objects.filter(name=new_deck_name, user=self.user).exists():
                # If the deck name is not unique, raise a validation error
                raise forms.ValidationError("A deck with this name already exists.")
            else:
                # Create a new deck
                new_deck = Deck.objects.create(name=new_deck_name, user=self.user)
                return new_deck
    
    def save(self, commit=True):
        card = super().save(commit=False)
        card.user = self.user
        if commit:
            with transaction.atomic():
                card.save()
                selected_decks = self.cleaned_data.get('decks')
                if not selected_decks:
                    selected_decks = [Deck.objects.get(name='default', user=self.user)]
                else:
                    # Check if 'default' is in selected_decks, and add it if not
                    default_deck = Deck.objects.get(name='default', user=self.user)
                    if default_deck not in selected_decks:
                        selected_decks = list(selected_decks) 
                        selected_decks.append(default_deck)                        
                for deck in selected_decks:
                    card.decks.add(deck)
        return card
    
    