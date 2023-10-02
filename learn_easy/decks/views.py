from django.shortcuts import render, HttpResponseRedirect
from .models import Deck
from cards.models import Card, Review
from .forms import DeckForm, AnswerForm
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django import forms


@login_required
def create_deck(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck_name = form.cleaned_data['deck_name']
            user = request.user  

            if deck_name.lower() == 'default':
                form.add_error('deck_name', 'You cannot create a deck with this deck_name.')
            else:
                deck = Deck(user=user, deck_name=deck_name)
                deck.save()
                return redirect('decks:deck_list') 
    else:
        form = DeckForm()

    return render(request, 'decks/create_deck.html', {'form': form})

@login_required
def deck_list(request):
    decks = Deck.objects.filter(user=request.user)
    return render(request, 'decks/deck_list.html', {'decks': decks})

@login_required
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)  
    cards = deck.cards.all()  # related_name='cards' in Cards to decks ManyToManyField
    available_cards = Card.objects.exclude(decks=deck)
    is_default_deck = deck.deck_name == 'default'
    return render(request, 'decks/deck_detail.html', {'deck': deck, 'cards': cards, 'available_cards': available_cards, 'is_default_deck': is_default_deck})


@login_required
def add_card_to_deck(request, deck_id):
    if request.method == 'POST':
        deck = get_object_or_404(Deck, id=deck_id)
        card_pk = request.POST.get('add_card')
        card = get_object_or_404(Card, pk=card_pk)
        deck.cards.add(card)
    return redirect('decks:deck_detail', deck_id=deck_id)

@login_required
def remove_card_from_deck(request, deck_id, card_pk):
    deck = get_object_or_404(Deck, pk=deck_id)
    card = get_object_or_404(Card, pk=card_pk)
    
    # Check if the deck is the 'default' deck
    is_default_deck = deck.deck_name == 'default'
    
    if request.method == 'POST':
        if is_default_deck:
            # Remove the card from the database
            card.delete()
        else:
            # Remove the card only from the specific deck
            deck.cards.remove(card)
            
    return redirect('decks:deck_detail', deck_id=deck_id)

def check_answer(answer):
    return True


def review_deck(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    cards = deck.get_cards_for_revision()
    if cards:
        card = cards[0]
        answer_submitted = False
        feedback = None
        outcome = None
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.cleaned_data.get('answer')
                # outcome, feedback = card.check_answer(answer)
                outcome, feedback = check_answer(answer), 'Sample Feedback'
                reviews = Review.objects.filter(card=card)
                
                if reviews.count() == 1:
                    review = reviews.first()
                else:
                    review = Review(card=card)

                review.update_review(outcome)
                answer_submitted = True
        else:
            form = AnswerForm()
        return render(request, 'decks/review.html', {'deck': deck, 'card': card, 'feedback': feedback, 'form': form, 'outcome':outcome, 'answer_submitted': answer_submitted})
    else:
        return redirect('decks:deck_list')


# show next review time, level for card
# set the question, feedback and answer checking API
# be able to skip card in review
# card_create page auto refresh
# django.db.utils.OperationalError: database is locked error handling
# what to do when you click review button and theres nothing to review

