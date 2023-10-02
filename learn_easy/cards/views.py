from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, Tag
from decks.models import Deck
from .forms import CardForm, AddCardToDeckForm, RemoveCardFromDeckForm, DeckForm
from django.contrib.auth.decorators import login_required 
from openai_API.api import OpenAI_API
from django.contrib import messages
from threading import Thread
from django.http import HttpResponseForbidden, JsonResponse
import openai
from .utils import send_ws_message_to_user_group
from django.db import transaction
from django.db import IntegrityError

ai = OpenAI_API()

@login_required
@transaction.atomic
def create_card(request):
    if request.method == 'POST':
        card_form = CardForm(request.POST, user=request.user)
        if card_form.is_valid():
            try:                
                card = card_form.save(commit=False)
                card.user = request.user
                card.save()
                card.decks.add(Deck.objects.get(user=request.user, deck_name='default'))
                selected_decks = card_form.cleaned_data['decks']
                for deck in selected_decks:
                    card.decks.add(deck)
                card.save()
                return redirect('cards:create_card')
            except IntegrityError:
                return JsonResponse({'error': 'A card with this name already exists.'})
            except Exception as e:
                return JsonResponse({'error': 'An error occurred while saving the card.'})
        else:
            return JsonResponse({'error': card_form.errors.as_json()})
    else:
        card_form = CardForm(user=request.user)
        deck_form = DeckForm()
    return render(request, 'cards/create_card.html', {'card_form': card_form, 'deck_form': deck_form})

@login_required
@transaction.atomic
def create_deck(request):
    if request.method == 'POST':
        deck_form = DeckForm(request.POST, user=request.user)
        if deck_form.is_valid():
            try:
                deck = deck_form.save(commit=False)
                deck.user = request.user
                deck.save()
                return JsonResponse({'deck_id': deck.id, 'deck_name': deck.deck_name})
            except IntegrityError:
                return JsonResponse({'error': 'A deck with this name already exists.'})
            except Exception as e:
                return JsonResponse({'error': 'An error occurred while saving the deck.'})
        else:
            return JsonResponse({'error': deck_form.errors.as_json()})
    else:
        deck_form = DeckForm(user=request.user)
    return JsonResponse({'error': 'Invalid request'})


@login_required
def create_card_helper(request, form):
    if form.is_valid():
        card = form.save(commit=False)
        card.user = request.user
        corrected_card_name = ai.spelling_corrector([card.card_name])[0]
        if Card.objects.filter(card_name__iexact=corrected_card_name, user=request.user).exists():
            messages.info(request, f'A card with the name "{card.card_name}" already exists.')
            return redirect('cards:create_card')
        card.card_name = corrected_card_name
        card.save() 
        messages.info(request, f'{card.card_name} saved successfully.')
        thread = Thread(target=get_meaning, args=(card, corrected_card_name, request))
        thread.start()     
        form.save()
        return redirect('cards:create_card')


def get_meaning(card, corrected_card_name, request):
    try:       
        system_defined_tag_names = ai.get_category(corrected_card_name)
        # Clear existing tags and add the new ones
        card.system_defined_tags.clear()
                
        for tag_name in system_defined_tag_names:            
            # Get or Create the Tag instance with the given name
            tag, created = Tag.objects.get_or_create(tag_name=tag_name.upper())  
            
            if created:
                tag.save()
                
            # Add the tag to the card's system_defined_tags
            card.system_defined_tags.add(tag)
        
        # meaning = ai.get_meaning(corrected_card_name)
        meaning = "SAMPLE MEANING TEXT"
        card.card_content_system_generated = meaning
        
        # Update card on card_list page
        # send_ws_message_to_user_group(request.user, message_type="card_update", data=card)
        
        card.save() 
        print("MEANING SAVED!")
        
    except openai.OpenAIError as e:        
        print(f'OPENAI API Error: {e}. {card.card_name} not saved.')
        card.delete()
        return redirect('cards:create_card')  # Redirect back to the form       


@login_required
def card_detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    
    if request.user != card.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit this card.")
    
    add_form = AddCardToDeckForm()
    add_form.fields['deck'].queryset = Deck.objects.exclude(cards=card)
    
    remove_form = RemoveCardFromDeckForm(user=request.user)
    remove_form.fields['deck'].queryset = card.decks.exclude(deck_name='default')
    
    return render(request, 'cards/card_detail.html', {'card': card, 'add_form': add_form, 'remove_form': remove_form})

@login_required
def card_list(request):
    cards = Card.objects.filter(user=request.user)
    response = render(request, 'cards/card_list.html', {'cards': cards})
    
    # Reloads the page when there is no-store even when we go back to this page from pressing the browsers back button
    response['Cache-Control'] = 'no-store'
    return response

@login_required
def delete_card(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.user != card.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this card.")
    card.delete()
    return redirect('cards:card_list')


@login_required
@transaction.atomic
def bulk_delete_card(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        selected_decks = request.POST.getlist('decks')
        deletion_option = request.POST.get('deletion_option')
        if deletion_option == 'all':
            # Delete the card from all decks
            card.delete()
            return redirect('cards:card_list')
        
        elif deletion_option == 'selected':
            # Delete the card only from selected decks
            card.decks.remove(*selected_decks)
            return redirect('cards:card_list')
    
    return render(request, 'cards/bulk_delete_card.html', {'card': card})


@login_required
def add_card_to_deck(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = AddCardToDeckForm(request.POST)
        form.fields['deck'].queryset = Deck.objects.exclude(cards=card)
        if form.is_valid():
            deck = form.cleaned_data['deck']
            deck.cards.add(card)
            return redirect('cards:card_detail', pk=card.pk)
    else:
        form = AddCardToDeckForm()
        form.fields['deck'].queryset = Deck.objects.exclude(cards=card)
        
    return redirect('cards:card_detail', pk=card.pk)

@login_required
def remove_card_from_deck(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = RemoveCardFromDeckForm(request.POST, user=request.user)
        if form.is_valid():
            deck = form.cleaned_data['deck']
            deck.cards.remove(card)
            return redirect('cards:card_detail', pk=card.pk)
    else:
        form = RemoveCardFromDeckForm(user=request.user)
        form.fields['deck'].queryset = card.decks.exclude(deck_name='default')
    return render(request, 'cards/card_detail.html', {'remove_form': form})