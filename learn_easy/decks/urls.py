from django.urls import path, include
from . import views

app_name = "decks"
urlpatterns = [
    path('create-deck/', views.create_deck, name='create_deck'),
    path('deck-list/', views.deck_list, name='deck_list'),
    path('deck/<int:deck_id>/', views.deck_detail, name='deck_detail'),
    path('<int:deck_id>/add_card/', views.add_card_to_deck, name='add_card_to_deck'),
    path('<int:deck_id>/remove_card/<int:card_pk>/', views.remove_card_from_deck, name='remove_card_from_deck'),
]