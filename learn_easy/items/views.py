from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required 
from openai_API.api import OpenAI_API
from django.contrib import messages
from threading import Thread
from django.http import HttpResponseForbidden
import openai
from .utils import send_ws_message_to_user_group

ai = OpenAI_API()

@login_required
def create_item(request):    
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            word = form.cleaned_data['word']
            messages.info(request, f'{word} saved successfully.')
            try:
                corrected_word = ai.spelling_corrector([word])[0]
                print(f"corrected_word:{corrected_word}")
                item.word = corrected_word
                item.save() 

                # Update item on item_list page
                send_ws_message_to_user_group(request.user, message_type="item_update", data=item)

                # Start thread to populate meaning
                thread = Thread(target=get_meaning, args=(item, corrected_word, request))
                thread.start()     
            except openai.OpenAIError as e:
                item.delete()  # Delete the item
                print(f'OPENAI API Error: {e}. {word} not saved.')
                messages.error(request, f'Server Error. {word} not saved.')  # Send error message
                return redirect('items:create_item')  # Redirect back to the form                          
            
            # Redirect to the same page
            return redirect('items:create_item')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form})

def get_meaning(item, corrected_word, request):
    try:       
        detected_category = ai.get_category(corrected_word)
        item.category = detected_category
        
        # Update item on item_list page
        send_ws_message_to_user_group(request.user, message_type="item_update", data=item)
        
        meaning = ai.get_meaning(corrected_word, detected_category)
        item.meaning = meaning
        
        # Update item on item_list page
        send_ws_message_to_user_group(request.user, message_type="item_update", data=item)
        
        item.save() 
        print("MEANING SAVED!")
        
    except openai.OpenAIError as e:        
        print(f'OPENAI API Error: {e}. {item.word} not saved.')
        item.delete()
        return redirect('items:create_item')  # Redirect back to the form       


@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user != item.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this item.")
    return render(request, 'items/item_detail.html', {'item': item})

@login_required
def item_list(request):
    items = Item.objects.filter(user=request.user)
    response = render(request, 'items/item_list.html', {'items': items})
    
    # Reloads the page when there is no-store even when we go back to this page from pressing the browsers back button
    response['Cache-Control'] = 'no-store'
    return response

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user != item.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this item.")
    item.delete()
    return redirect('items:item_list')