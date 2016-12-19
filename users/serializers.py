from django.contrib.auth import authenticate
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


class UserSignInSerializer(serializers.Serializer):
    email = serializers.CharField(label='email')
    password = serializers.CharField(
        label='Password', style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
