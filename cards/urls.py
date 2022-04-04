from django.urls import path
from .views import card, add_card, remove_cart, remove_cart_item

urlpatterns = [
    path('',card,name='card'),
    path('add_cart/<int:product_id>/',add_card,name="add_cart"),
    path('minus_card/<int:product_id>/<int:cart_item_id>/',remove_cart,name="minus_card"),
    path('delete_card_item/<int:product_id>/<int:cart_item_id>/',remove_cart_item,name="delete_card_item"),
    
]
