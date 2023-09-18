from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required  # Import login_required decorator

@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items})

@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('items:item_list')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form})

@login_required
def delete_item(request, pk):
    item = Item.objects.get(pk=pk)
    item.delete()
    return redirect('items:item_list')