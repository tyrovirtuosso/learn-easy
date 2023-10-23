from django import forms
from .models import Deck
from cards.models import Review, Card

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['deck_name']
        
class AnswerForm(forms.Form):
    answer = forms.CharField()
    ease_of_recall = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())
        