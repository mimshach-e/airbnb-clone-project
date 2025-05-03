# Importing required and necessary functions and classes
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView

# URL patterns for the user account management views
urlpatterns = [
    # Account Management URLs
    path('account/register/', UserRegistrationView.as_view(), name='register'),
    path('account/login/', UserLoginView.as_view(), name='login'),
    path('account/profile/', UserProfileView.as_view(), name='profile'),

]