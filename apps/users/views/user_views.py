from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404)
from rest_framework.views import APIView
from rest_framework import status

from apps.users.models import User
from apps.users.serializers import (UserRegistrationSerializer, UserDetailSerializer, UserLoginSerializer)
from apps.users.permissions import IsOwner

class UserRegistrationAPIView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class UserLoginAPIView(APIView):

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {
                    'detail': 'Login successful',
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'error': 'Invalid Credentials',
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserLogoutAPIView(APIView):

    def post(self, request):
        logout(request)
        return Response(
            {
                'detail': 'Logout successful',
            },
            status=status.HTTP_200_OK
        )


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserRegistrationSerializer
        elif self.request.method == 'GET':
            return UserDetailSerializer