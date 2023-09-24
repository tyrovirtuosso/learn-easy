from django.urls import path, include
from . import views

app_name = "cards"
urlpatterns = [
    path('list/', views.card_list, name='card_list'),
    path('create/', views.create_card, name='create_card'),
    path('delete/<int:pk>/', views.delete_card, name='delete_card'),
    path('card/<int:pk>/', views.card_detail, name='card_detail'),
]