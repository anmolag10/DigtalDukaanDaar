from django.urls import path, include
from . import views as customerViews

urlpatterns = [
    path('pin_filter/', customerViews.postPinFilter, name = "post-pin-filter"),
    path('cart/', customerViews.cartView, name = 'cust-cart-page'),
    path('stores/', customerViews.storesView, name = 'cust-stores-page'),
    path('items/', customerViews.itemsView, name = 'cust-items-page'),
]