# Importing modules, functions and classes
from django.urls import include, path
from .views import ListCreateAmenitiesView, RetrieveUpdateDeleteAmenitiesView, ListCreatePropertyView, DetailProductView, ReviewView


urlpatterns = [
    path('/amenities/', ListCreateAmenitiesView.as_view(), name='list-create'),
    path('/amenities/<int:pk>/', RetrieveUpdateDeleteAmenitiesView.as_view(), name='details'),

    path('/properties/', ListCreatePropertyView.as_view(), name='list-create'),
    path('/properties/<int:pk>/', DetailProductView.as_view(), name='details'),

    path('/reviews/',)


]