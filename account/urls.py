# Importing required and necessary functions and classes
from django.urls import path

from .views import UserLoginView, UserProfileView, ListRegisterUserView

# URL patterns for the user account management views
urlpatterns = [
    # Account Management URLs
    path('users/', ListRegisterUserView.as_view(), name='register'),
    path('users/login/', UserLoginView.as_view(), name='login'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='profile'),

]