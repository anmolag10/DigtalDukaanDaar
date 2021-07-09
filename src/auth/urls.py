from django.urls import path
from . import views as signViews

urlpatterns = [
    path('', signViews.authView, name ='auth-page'),
    path('<is_signin>/', signViews.postAuthView, name='post-auth')
]