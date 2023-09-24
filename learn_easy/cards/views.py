from django.shortcuts import render, redirect, get_object_or_404
from .models import Card
from .forms import CardForm
from django.contrib.auth.decorators import login_required 
from openai_API.api import OpenAI_API
from django.contrib import messages
from threading import Thread
from django.http import HttpResponseForbidden
import openai
from .utils import send_ws_message_to_user_group

ai = OpenAI_API()

@login_required
def create_card(request):    
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            word = form.cleaned_data['word']
            messages.info(request, f'{word} saved successfully.')
            try:
                corrected_word = ai.spelling_corrector([word])[0]
                print(f"corrected_word:{corrected_word}")
                card.word = corrected_word
                card.save() 

                # Update card on card_list page
                send_ws_message_to_user_group(request.user, message_type="card_update", data=card)

                # Start thread to populate meaning
                thread = Thread(target=get_meaning, args=(card, corrected_word, request))
                thread.start()     
            except openai.OpenAIError as e:
                card.delete()  # Delete the card
                print(f'OPENAI API Error: {e}. {word} not saved.')
                messages.error(request, f'Server Error. {word} not saved.')  # Send error message
                return redirect('cards:create_card')  # Redirect back to the form                          
            
            # Redirect to the same page
            return redirect('cards:create_card')
    else:
        form = CardForm()
    return render(request, 'cards/card_form.html', {'form': form})

def get_meaning(card, corrected_word, request):
    try:       
        detected_category = ai.get_category(corrected_word)
        card.category = detected_category
        
        # Update card on card_list page
        send_ws_message_to_user_group(request.user, message_type="card_update", data=card)
        
        meaning = ai.get_meaning(corrected_word, detected_category)
        card.meaning = meaning
        
        # Update card on card_list page
        send_ws_message_to_user_group(request.user, message_type="card_update", data=card)
        
        card.save() 
        print("MEANING SAVED!")
        
    except openai.OpenAIError as e:        
        print(f'OPENAI API Error: {e}. {card.word} not saved.')
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


