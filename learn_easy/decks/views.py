from django.shortcuts import render
from .models import Deck
from .forms import DeckForm
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def create_deck(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user = request.user  

            if name.lower() == 'default':
                form.add_error('name', 'You cannot create a deck with this name.')
            else:
                deck = Deck(user=user, name=name)
                deck.save()
                return redirect('deck_list') 
    else:
        form = DeckForm()

    return render(request, 'deck/create_deck.html', {'form': form})

@login_required
def deck_list(request):
    decks = Deck.objects.filter(user=request.user)
    return render(request, 'deck/deck_list.html', {'decks': decks})

@login_required
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)  # Assuming you're using authentication
    return render(request, 'deck/deck_detail.html', {'deck': deck})