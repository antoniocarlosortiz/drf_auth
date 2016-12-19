from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer


class UserView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
