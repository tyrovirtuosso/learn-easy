from django.shortcuts import render, HttpResponseRedirect
from .models import Deck
from cards.models import Card, Review
from .forms import DeckForm, ReviewForm
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib import messages


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


class ReviewView(View):
    def get(self, request, deck_id):
        deck = Deck.objects.get(id=deck_id)
        cards = deck.get_cards_for_revision()
        if cards:
            card = cards.first()
            form = ReviewForm(initial={'card': card.id})
            # Check if there are any cards left for review
            show_next_button = cards.count() > 1
            return render(request, 'decks/review.html', {'form': form, 'card': card, 'deck_id': deck_id, 'show_next_button': show_next_button})
        else:
            messages.info(request, 'No more cards to review.')
            return redirect(reverse('decks:deck_list'))

    def post(self, request, deck_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            card = Card.objects.get(id=form.cleaned_data['card'].id)
            answer = form.cleaned_data['answer']
            outcome, feedback = True, 'sample feedback'
            
            reviews = Review.objects.filter(card=card)
            if reviews.count() == 1:
                review = reviews.first()
            else:
                review = Review(card=card)
            
            review.update_review(outcome, True)
            
            # Get the deck again and check if there are any cards left for review
            deck = Deck.objects.get(id=deck_id)
            cards = deck.get_cards_for_revision()
            show_next_button = cards.count() > 0

            context = {
                'form': form,
                'card': card,
                'outcome': outcome,
                'feedback': feedback,
                'show_next_button': show_next_button,
                'deck_id': deck_id,
            }
            return render(request, 'decks/review.html', context)



# show next review time, level for card
# set the question, feedback and answer checking API

# card_create page auto refresh
# django.db.utils.OperationalError: database is locked error handling
# what to do when you click review button and theres nothing to review

