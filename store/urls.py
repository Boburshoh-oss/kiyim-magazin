from django.urls import path
from .views import store,product_detail,search

urlpatterns = [
    path('',store,name='store'),
    path('category/<slug:cat_slug>/',store,name='detail_category'),
    path('category/<slug:cat_slug>/<slug:product_slug>',product_detail,name='product_detail'),
    path('search/',search,name="search")
]
