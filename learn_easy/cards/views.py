from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, Tag
from decks.models import Deck
from .forms import CardForm
from django.contrib.auth.decorators import login_required 
from openai_API.api import OpenAI_API
from django.contrib import messages
from threading import Thread
from django.http import HttpResponseForbidden
import openai
from .utils import send_ws_message_to_user_group
from django.db import transaction
from django.db import IntegrityError

ai = OpenAI_API()

@login_required
@transaction.atomic
def create_card(request):    
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = CardForm(user=request.user, data=request.POST)
        if form.is_valid():
            card_name = form.cleaned_data['card_name']
            try:
                corrected_card_name = ai.spelling_corrector([card_name])[0]
                print(f"corrected_card_name:{corrected_card_name}")
                                
                # Check if a card with the same card_name already exists
                if Card.objects.filter(card_name__iexact=corrected_card_name, user=request.user).exists():
                    if card_name.lower() == corrected_card_name.lower():
                        messages.info(request, f'A card with the name "{card_name}" already exists.')
                    else:
                        messages.info(request, f'A card with the corrected name "{corrected_card_name}" already exists.')
                    return redirect('cards:create_card')
                
                card = form.save(commit=False)  # Save the card but don't commit it to the database yet
                card.user = request.user
                
                card.card_name = corrected_card_name
                card.save() 
                
                selected_decks = form.cleaned_data['decks']
                print(f"selected_decks:{selected_decks}")
                
                messages.info(request, f'{card_name} saved successfully.')
                
                # Start thread to populate meaning
                thread = Thread(target=get_meaning, args=(card, corrected_card_name, request))
                thread.start()     
                form.save()  # This will commit the changes made in the form's save method

            except openai.OpenAIError as e:
                card.delete()  # Delete the card
                print(f'OPENAI API Error: {e}. {card_name} not saved.')
                messages.error(request, f'Server Error. {card_name} not saved.')  # Send error message
                return redirect('cards:create_card')  # Redirect back to the form                          
            
            except IntegrityError:
                messages.error(request, 'This card is already in the selected deck(s).')
                return redirect('cards:create_card')
            
            # Redirect to the same page
            return redirect('cards:create_card')
    else:
        form = CardForm(user=request.user)
    return render(request, 'cards/card_form.html', {'form': form})

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
        return HttpResponseForbidden("You are not allowed to delete this card.")
    return render(request, 'cards/card_detail.html', {'card': card})

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


