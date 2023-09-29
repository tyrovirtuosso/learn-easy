from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, Tag
from decks.models import Deck
from .forms import CardForm, CardDeckCreationForm, AddCardToDeckForm, RemoveCardFromDeckForm
from django.contrib.auth.decorators import login_required 
from openai_API.api import OpenAI_API
from django.contrib import messages
from threading import Thread
from django.http import HttpResponseForbidden
import openai
from .utils import send_ws_message_to_user_group
from django.db import transaction

ai = OpenAI_API()

@login_required
@transaction.atomic
def create_card(request):    
    storage = messages.get_messages(request)
    storage.used = True
    
    card_deck_creation_form = CardDeckCreationForm(request.POST or None)
    card_form = CardForm(request.POST or None, user=request.user)
    if request.method == 'POST':
        print(request.POST)
        if 'deck_name' in request.POST:
            create_deck(request, card_deck_creation_form)
        else:   
            create_card_helper(request, card_form)
    
    return render(request, 'cards/card_form.html', {'card_deck_creation_form': card_deck_creation_form, 'form': card_form})

@login_required
def create_deck(request, form):
    if form.is_valid():
        new_deck = form.save(commit=False)
        new_deck.user = request.user
        if Deck.objects.filter(deck_name=new_deck.deck_name, user=request.user).exists():
            messages.error(request, "A deck with this deck_name already exists.")
        else:
            new_deck.save()
            messages.success(request, f"Deck '{new_deck.deck_name}' created successfully.")
            return redirect('cards:create_card')

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