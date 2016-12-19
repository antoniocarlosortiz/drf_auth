from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name',
            'email', 'password', 'is_active')
        extra_kwargs = {
                'password': {'write_only': True}
        }

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        user.send_confirm_email()
        return user
