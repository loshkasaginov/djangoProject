from django.urls import path
from . import views
from .views import clear_cart

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
]
