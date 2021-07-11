from django.urls import path, include
from . import views as nonUserViews

urlpatterns = [
    path('', nonUserViews.redirectHome),
    path('logout/', nonUserViews.logout, name = 'logout'),
    path('home/', nonUserViews.homeView, name = 'home-page'),
    path('items/', nonUserViews.itemsView, name = 'home-items-page'),
    path('search/', nonUserViews.searchView, name = 'search-page'),
    path('profile/', nonUserViews.profileView, name = 'profile-page'),
]