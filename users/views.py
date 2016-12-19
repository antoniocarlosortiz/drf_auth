from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from .serializers import UserSignInSerializer


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
    def post(self, request, *args, **kwargs):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
