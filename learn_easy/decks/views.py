from django.shortcuts import render, HttpResponseRedirect
from .models import Deck
from cards.models import Card, Review, Level
from .forms import DeckForm, AnswerForm
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django import forms
import time
from django.utils import timezone
from openai_API.api import OpenAI_API

ai = OpenAI_API()


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
    cards = deck.cards_deck.all()
    available_cards = Card.objects.exclude(decks=deck)
    is_default_deck = deck.deck_name == 'default'
    return render(request, 'decks/deck_detail.html', {'deck': deck, 'cards': cards, 'available_cards': available_cards, 'is_default_deck': is_default_deck})


@login_required
def add_card_to_deck(request, deck_id):
    if request.method == 'POST':
        deck = get_object_or_404(Deck, id=deck_id)
        card_pk = request.POST.get('add_card')
        card = get_object_or_404(Card, pk=card_pk)
        deck.cards_deck.add(card)
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

# put priority level on card model rather than review model.
@login_required
def review_deck(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    cards = deck.get_cards_for_revision()
    if cards:
        card = cards[0]
        answer_submitted = False
        feedback = None
        outcome = None
        completion_time = None
        question = card.review_set.latest('next_review').question
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                latest_review = Review.objects.filter(card=card).latest('next_review')
                question = latest_review.question
                answer = form.cleaned_data.get('answer')
                outcome, feedback = ai.check_answer(question, answer)
                completion_time = float(request.POST.get('completion_time'))
                answer_submitted = True
                ease_of_recall = form.cleaned_data.get('ease_of_recall')
                
                priority_level = False # Currently hardcoded, but ask user for input.
                
                latest_review.update_review(card, outcome, ease_of_recall, priority_level, completion_time)

        else:
            form = AnswerForm()
        return render(request, 'decks/review.html', {
            'deck': deck,
            'card': card,
            'question': question,
            'feedback': feedback,
            'form': form,
            'outcome':outcome,
            'answer_submitted': answer_submitted,
            'completion_time': completion_time
            })
    else:
        return redirect('decks:deck_list')



