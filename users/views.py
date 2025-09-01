from django.shortcuts import render

from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
