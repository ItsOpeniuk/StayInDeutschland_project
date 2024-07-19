from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status

from apps.users.serializers import UserRegistrationSerializer, UserDetailSerializer, UserLoginSerializer
from apps.users.permissions import IsOwner


class UserRegistrationAPIView(CreateAPIView):
    """
    View for user registration.

    This view allows new users to register by providing their details.

    Permissions:
        - `AllowAny`: Anyone can access this view to create a new user.

    Methods:
        POST:
            - Request body must contain user registration data.
            - Returns a 201 Created response with user data on successful registration.
            - Raises a 400 Bad Request response if registration data is invalid.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Handle POST request to register a new user.

        Args:
            request (Request): The request object containing user registration data.

        Returns:
            Response: A response with the serialized user data and HTTP 201 Created status.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class UserLoginAPIView(APIView):
    """
    View for user login.

    This view allows users to log in by providing their email and password.

    Permissions:
        - `AllowAny`: Anyone can access this view to log in.

    Methods:
        POST:
            - Request body must contain 'email' and 'password'.
            - Returns a 200 OK response with a success message on successful login.
            - Returns a 401 Unauthorized response with an error message if credentials are invalid.
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to log in a user.

        Args:
            request (Request): The request object containing 'email' and 'password'.

        Returns:
            Response: A response with a success message and HTTP 200 OK status on successful login,
                      or an error message and HTTP 401 Unauthorized status if login fails.
        """
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
    """
    View for user logout.

    This view allows logged-in users to log out.

    Permissions:
        - `IsAuthenticated`: Only authenticated users can access this view.

    Methods:
        POST:
            - Logs out the currently authenticated user.
            - Returns a 200 OK response with a success message.
    """

    def post(self, request):
        """
        Handle POST request to log out the currently authenticated user.

        Args:
            request (Request): The request object.

        Returns:
            Response: A response with a success message and HTTP 200 OK status.
        """
        logout(request)
        return Response(
            {
                'detail': 'Logout successful',
            },
            status=status.HTTP_200_OK
        )


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete the currently authenticated user's details.

    Permissions:
        - `IsAuthenticated`: Only authenticated users can access this view.
        - `IsOwner`: Ensures that only the user themselves can access or modify their own data.

    Methods:
        GET:
            - Retrieves the details of the currently authenticated user.

        PUT/PATCH:
            - Updates the details of the currently authenticated user.

        DELETE:
            - Deletes the currently authenticated user's account.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UserDetailSerializer

    def get_object(self):
        """
        Retrieve the currently authenticated user.

        Returns:
            User: The currently authenticated user instance.
        """
        return self.request.user
