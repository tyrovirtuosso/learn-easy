from django.urls import path, include
from . import views

app_name = "items"
urlpatterns = [
    path('list/', views.item_list, name='item_list'),
    path('create/', views.create_item, name='create_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
]