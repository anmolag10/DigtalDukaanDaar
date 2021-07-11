from django.urls import path, include
from . import views as customerViews

urlpatterns = [
    path('cart/', customerViews.cartView, name = 'cust-cart-page'),
    path('stores/<store_id>/', customerViews.storesView, name = 'cust-stores-page'),
    path('items/', customerViews.itemsView, name = 'cust-items-page'),
]