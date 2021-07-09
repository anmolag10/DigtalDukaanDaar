from django.urls import path, include
from . import views as retailerViews

urlpatterns = [
    path('cart/', retailerViews.cartView, name = 'ret-cart-page'),
    path('supplies/', retailerViews.supplyView, name = 'ret-supply-page'),
    path('items/', retailerViews.itemsView, name = 'ret-items-page'),
    path('manage_items/', retailerViews.manageItemView, name = 'ret-manage-page'),
    path('analytics/', retailerViews.analyticsView, name = 'ret-analytics'),
]