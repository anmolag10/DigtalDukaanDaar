from django.urls import path, include
from . import views as retailerViews

urlpatterns = [
    path('cart/', retailerViews.cartView, name = 'ret-cart-page'),
    path('supplies/', retailerViews.storesView, name = 'ret-supply-page'),
    path('items/', retailerViews.itemsView, name = 'ret-items-page'),
    path('manage_store', retailerViews.manageStoreView, name = 'ret-manage-page'),
]