from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from cards.models import CardItem
from .models import Product
from category.models import Category
from cards.views import _card_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def store(request, cat_slug=None):
    categories = None
    products = None
    
    if cat_slug != None:
        categories = get_object_or_404(Category,slug=cat_slug)
        products = Product.objects.filter(category = categories,is_available=True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    context = {
        "products":paged_products,
        "products_count":products_count
    }
    return render(request,'store/store.html',context)

def product_detail(request,cat_slug,product_slug):
    try:
        product = Product.objects.get(category__slug=cat_slug,slug=product_slug)
        in_cart = CardItem.objects.filter(card__card_id=_card_id(request),product=product).exists()
    except Exception as e:
        raise e
    context = {
        "single_product":product,
        "in_cart":in_cart
    }
    return render(request,'store/product_detail.html',context)

def search(request):
    products_count = 0
    products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
            products_count = products.count()
    context = {
        'products':products,
        'products_count':products_count
    }
    return render(request,'store/store.html',context)