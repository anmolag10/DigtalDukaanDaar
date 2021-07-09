from django.urls import path, include
from . import views as supplierViews

urlpatterns = [
    path('bid/', supplierViews.bidView, name = 'sup-bid-page'),
    path('manage_store', supplierViews.manageStoreView, name = 'sup-manage-page'),
]