from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .serializers import *
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import check_password
from rest_framework import status, views, permissions
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer
from bloomfilter.models import BloomFilterModel
from bloomfilter.utils import BloomFilter
from .models import User

#Register a new user to the aplication
#The function checks the password if it is in the bloom filter to determine if its weak/leaked first
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('current-user'))
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('current-user'))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password')

        # Determine which Bloom filter to use based on password length
        if len(password) >= 8 and len(password) <= 10:
            bloom_filter_id = 12
        elif len(password) > 10:
            bloom_filter_id = 13
        else:
            bloom_filter_id = 14

        # Check the password with the bloom filter vector
        try:
            bf_model = BloomFilterModel.objects.get(pk=bloom_filter_id)
            bf = BloomFilter.load_from_model(bf_model)
            threshold = 0.827  # You can set this threshold as needed
            if bf.check(password, threshold):
                return Response({'error': 'Password is too weak, choose a stronger one'}, status=status.HTTP_400_BAD_REQUEST)
        except BloomFilterModel.DoesNotExist:
            return Response({'error': 'Bloom filter not found'}, status=status.HTTP_404_NOT_FOUND)

        # Save the user
        self.perform_create(serializer)

        # Add the password to the Bloom filter
        bf.add(password)
        bf.save_to_model(bf_model)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

#Login am existent user to the application
class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('current-user'))
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('current-user'))
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            login(request, user)
            return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
#Shows the user information
class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
#Logout a signed in user from the application
class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

#Changin a password function to an existent user that is logged in
#the function will check if the password is leaked/weak, or if the new password is just sligtly modified
class ChangePasswordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Check if old password is correct
            if not user.check_password(old_password):
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

            # Determine which Bloom filter to use based on new password length
            if len(new_password) >= 8 and len(new_password) <= 10:
                bloom_filter_id = 12
            elif len(new_password) > 10:
                bloom_filter_id = 13
            else:
                bloom_filter_id = 14

            # Check the new password against the appropriate Bloom filter
            try:
                bf_model = BloomFilterModel.objects.get(pk=bloom_filter_id)
                bf = BloomFilter.load_from_model(bf_model)
                threshold = 0.827  # You can set this threshold as needed
                if bf.check(new_password, threshold):
                    return Response({'error': 'Password is too weak, choose a stronger one'}, status=status.HTTP_400_BAD_REQUEST)
            except BloomFilterModel.DoesNotExist:
                return Response({'error': 'Bloom filter not found'}, status=status.HTTP_404_NOT_FOUND)

            # Change the password
            
            user.set_password(new_password)
            bf.add(new_password)
            bf.save_to_model(bf_model)
            user.save()
            return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
