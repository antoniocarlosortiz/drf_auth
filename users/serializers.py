from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        hidden_fields = kwargs['context'].pop('hidden_fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if hidden_fields:
            hidden_fields = set(hidden_fields)
            for field_name in hidden_fields:
                self.fields.pop(field_name)

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

        attrs['user'] = user
        return attrs


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        label='Password', style={'input_type': 'password'})
