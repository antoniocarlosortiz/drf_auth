from djang.conf import settings
from django.shortcuts import render

from serializers import UserSerializer


class UserView(CreateAPIView):
    model = settings.AUTH_USER_MODEL
    serializer_class = UserSerializer
