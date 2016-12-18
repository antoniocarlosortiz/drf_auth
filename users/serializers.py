from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('url', 'id', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        User = get_user_model()
        user = User.create_user(**validated_data)
        return user
