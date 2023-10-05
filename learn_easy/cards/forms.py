from django import forms
from .models import Card, Tag
from decks.models import Deck
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name']
        # exclude = ['user', "decks", "smart_decks", "system_defined_tags", "user_defined_tags", "card_content_system_generated", "card_content_user_generated", "notes", "associated_resources", "pronunciation"]
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CardForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        card_name = cleaned_data.get('card_name').lower()
        if Card.objects.filter(card_name=card_name, user=self.user).exists():
            print("A card with this name already exists.")
            raise ValidationError("A card with this name already exists.")
        
    
    def save(self, commit=True):
        card = super().save(commit=False)
        card.user = self.user
        if commit:
            card.save()
            try:
                default_deck = Deck.objects.get(user=self.user, deck_name='default')
                card.decks.add(default_deck)
                card.save()
            except Deck.DoesNotExist:
                card.delete()
                raise ValidationError("Failed to add the default deck to the card.")
        return card
        


# class CardForm(forms.ModelForm):
#     decks = forms.ModelMultipleChoiceField(queryset=Deck.objects.none(), required=False)
#     card_content_user_generated = forms.CharField(required=False)

#     class Meta:
#         model = Card
#         exclude = ['user', "system_defined_tags", "user_defined_tags", "card_content_system_generated", "associated_resources", "pronunciation", "notes"]

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super(CardForm, self).__init__(*args, **kwargs)
#         self.fields['decks'].queryset = Deck.objects.filter(user=self.user).exclude(deck_name='default')

#     def clean(self):
#         cleaned_data = super().clean()
#         card_name = cleaned_data.get('card_name')
#         print(card_name)
#         if card_name:
#             card_name = card_name.lower()
#         if Card.objects.filter(card_name=card_name, user=self.user).exists():
#             raise ValidationError("A card with this name already exists.")

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['deck_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DeckForm, self).__init__(*args, **kwargs)

    def clean_deck_name(self):
        deck_name = self.cleaned_data.get('deck_name').lower()
        print(deck_name)
        if Deck.objects.filter(deck_name=deck_name, user=self.user).exists():
            print("in deck_name error")
            raise ValidationError("A deck with this name already exists.")
    
class AddCardToDeckForm(forms.Form):
    deck = forms.ModelChoiceField(queryset=Deck.objects.none())

class RemoveCardFromDeckForm(forms.Form):
    deck = forms.ModelChoiceField(queryset=Deck.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RemoveCardFromDeckForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['deck'].queryset = user.deck_set.exclude(deck_name='default')
            
class CardEditForm(forms.ModelForm):
    user_defined_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    
    new_user_defined_tags = forms.CharField(
        max_length=255,
        required=False,  # This field is optional
        help_text="Add new user-defined tags, separated by commas"
    )
    
    class Meta:
        model = Card
        fields = ['card_name', 'card_content_system_generated', 'card_content_user_generated', 'notes', 'user_defined_tags']