from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required 
from openai_API.api import OpenAI_API
from django.contrib import messages
from threading import Thread
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

ai = OpenAI_API()


@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            word = form.cleaned_data['word']
            messages.success(request, f'{word} saved successfully.')
            
            corrected_word = ai.spelling_corrector([word])[0]
            print(f"corrected_word:{corrected_word}")
            item.word = corrected_word
            item.save()
            
            # Send notification
            channel_layer = get_channel_layer()
            print(channel_layer)
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "message": f"Word {corrected_word} saved!",
                    "item_id": item.id,
                    "category": None,  # No category yet
                    "word": corrected_word  # Include the word
                }
            )
                        
            # Start thread to populate meaning
            thread = Thread(target=get_meaning, args=(item, corrected_word))
            thread.start()                               
            
            # Redirect to the same page
            return redirect('items:create_item')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form})

def get_meaning(item, corrected_word):
    detected_category = ai.get_category(corrected_word)
    meaning = ai.get_meaning(corrected_word, detected_category)
    item.category = detected_category
    item.meaning = meaning
    item.save() 
    print("MEANING SAVED!")
    # Send notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": f"Meaning for {corrected_word} saved!",
            "item_id": item.id,
            "category": detected_category, 
            "word": corrected_word 
        }
    )


@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
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
    item = Item.objects.get(pk=pk)
    item.delete()
    return redirect('items:item_list')