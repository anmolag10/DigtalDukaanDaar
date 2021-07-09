from django.urls import path, include
from . import views as authViews

urlpatterns = [
    path('supplier/<is_signin>/', authViews.supAuthView, name = "sup-auth-page"),
    path('retailer/<is_signin>/', authViews.retAuthView, name = "ret-auth-page"),
    path('customer/<is_signin>/', authViews.custAuthView, name = "cust-auth-page"),
]