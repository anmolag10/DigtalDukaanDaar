from django.urls import path, include
from . import views as supplierViews

urlpatterns = [
    path('bid/', supplierViews.bidView, name = 'sup-bid-page'),
    path('manage_items/', supplierViews.manageItemView, name = 'sup-manage-items-page'),
    path('analytics/', supplierViews.analyticsView, name = 'sup-analytics')
]