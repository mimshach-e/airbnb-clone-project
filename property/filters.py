# Importing classes
from django_filters.rest_framework import FilterSet

from .models import Property

# Property Filter Class

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'amenities': ['exact'],
            'price': ['gte', 'lte'],
        }
