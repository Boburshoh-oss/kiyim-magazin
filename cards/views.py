from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, Variation
from .models import Card, CardItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _card_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
    
def add_card(request,product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
                print(variation)
            except:
                pass
    
    try:
        cart = Card.objects.get(card_id=_card_id(request))
    except Card.DoesNotExist:
        cart = Card.objects.create(
            card_id = _card_id(request)
        )
    cart.save()
    is_cart_item_exists = CardItem.objects.filter(product=product,card=cart).exists()
    if is_cart_item_exists:
        cart_item = CardItem.objects.filter(product=product,card=cart)
        
        ex_var_list = []
        id = []
        for it in cart_item:
            existing_variation = it.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(int(it.id))
        print(ex_var_list)
        
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CardItem.objects.get(product=product,id=item_id)
            item.quantity += 1
            item.save()
        else:
            cart_item = CardItem.objects.create(product=product,quantity=1,card=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear() 
                cart_item.variations.add(*product_variation)
        # cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item = CardItem.objects.create(
            product=product,
            quantity = 1,
            card = cart
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    
    return redirect('card')

def remove_cart(request,product_id,cart_item_id):
    cart = Card.objects.get(card_id=_card_id(request))
    product = get_object_or_404(Product,id=product_id)
    try:
        cart_item = CardItem.objects.get(product=product,card=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('card')    

def remove_cart_item(request,product_id,cart_item_id):
    cart = Card.objects.get(card_id=_card_id(request))
    product = get_object_or_404(Product,id=product_id)
    try:
        cart_item = CardItem.objects.get(product=product,card=cart,id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('card')    
    
def card(request,total=0,quantity=0):
    
    try:
        tax = 0
        grand_total = 0
        cart = Card.objects.get(card_id=_card_id(request))
        cart_items = CardItem.objects.filter(card=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,"store/card.html",context)