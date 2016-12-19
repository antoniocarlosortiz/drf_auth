from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from .serializers import UserSignInSerialzer


class UserView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer


class UserConfirmView(APIView):
    def get(self, request, format=None):
        confirm_key = request.GET.get('code')
        if not confirm_key:
            errors = {'user': 'No confirm code found.'}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()

        try:
            user = User.objects.get(confirm_key=confirm_key)
        except User.DoesNotExist:
            errors = {'user': 'User not found.'}
            return Response(errors, status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignInView(APIView):
    def post(self, request, format=None):
        serializer = UserSignInSerialzer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.create(user=user)
            content = {'token': token}
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
