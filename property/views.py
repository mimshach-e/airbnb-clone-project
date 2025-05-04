# Importing modules and classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import PropertyFilter
from .models import Amenities, Property, Review
from .serializers import AmenitiesSerializer, PropertySerializer, ReviewSerializer

# Create Amenities View

class ListCreateAmenitiesView(generics.ListCreateAPIView):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



# Detail Amenities View

class RetrieveUpdateDeleteAmenitiesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]



# Create Property View

class ListCreatePropertyView(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by('created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]
    

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter

    # Allows for partial matches in property names for flexible search results.
    search_fields = ['name', 'amenities__name']

    # Allows for ordering property list by the date posted
    ordering_fields = ['created_at']

    # Handles pagination for property list, only 10 products are displayed per page
    pagination_class = PageNumberPagination

# Detail Products View

class DetailProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)




# Review View

class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Querying the Review model to get each property by filtering with ID
    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        if property_id:
            return Review.objects.filter(property_id=property_id).order_by('-created_at')
        return Review.objects.none()

    # Creating a context for the Serializer class
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        context['property_id'] = self.kwargs.get('property_id')
        return context