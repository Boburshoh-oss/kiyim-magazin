from .models import Card, CardItem
from .views import _card_id
def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Card.objects.filter(card_id=_card_id(request))
            if request.user.is_authenticated:
                cart_items = CardItem.objects.all().filter(user=request.user)
            else:
                cart_items = CardItem.objects.all().filter(card=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Card.DoesNotExist:
            cart_count = 0
        
    return dict(cart_count=cart_count)