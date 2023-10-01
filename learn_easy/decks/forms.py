from django import forms
from .models import Deck
from cards.models import Review, Card

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['deck_name']
        
class ReviewForm(forms.Form):
    card = forms.ModelChoiceField(queryset=Card.objects.all(), widget=forms.HiddenInput())
    answer = forms.CharField()