from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .serializers import UserSerializer
from .serializers import UserSignInSerializer
from .serializers import UserChangePasswordSerializer


class UserView(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    hidden_fields = ('email', 'last_name')

    def get_serializer_context(self):
        context = super(UserView, self).get_serializer_context()
        if (self.request.method in permissions.SAFE_METHODS and
                not self.request.user.is_authenticated):
            context['hidden_fields'] = self.hidden_fields
        return context


class UserDetailView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    hidden_fields = ('email', 'last_name')

    def get_serializer_context(self):
        context = super(UserDetailView, self).get_serializer_context()
        if (self.request.method in permissions.SAFE_METHODS and
                not self.request.user.is_authenticated):
            context['hidden_fields'] = self.hidden_fields
        return context


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
        return Response()


class UserSignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response()
