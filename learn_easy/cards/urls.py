from django.urls import path, include
from . import views

app_name = "cards"
urlpatterns = [
    path('list/', views.card_list, name='card_list'),
    path('create/', views.create_card, name='create_card'),
    path('delete/<int:pk>/', views.delete_card, name='delete_card'),
    path('card/<int:pk>/', views.card_detail, name='card_detail'),
    path('bulk_delete_card/<int:pk>/', views.bulk_delete_card, name='bulk_delete_card'),
    path('card/<int:pk>/add_to_deck/', views.add_card_to_deck, name='add_card_to_deck'),
    path('card/<int:pk>/remove_from_deck/', views.remove_card_from_deck, name='remove_card_from_deck'),

]