# Importing required and necessary modules, functions and classes
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer


# User Registration View: A view to register new users
class ListRegisterUserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    # A function to validate user data for registration
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# User Login View: A view for users to login into their accounts
class UserLoginView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]


# A function to validate user data
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])

        # Check if user is active and login the user and then return the data of the user
        if user and user.is_active:
            login(request, user)
            return Response({
                'id': user.id,
                'message': f'Login successful. Welcome {user.username}'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    
# User Profile View: A view for users to view their account details
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
