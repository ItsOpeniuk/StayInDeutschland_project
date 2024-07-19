from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    get_object_or_404,
    ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.rental_announcement.choices.booking_status import BookingStatus
from apps.rental_announcement.models import Booking
from apps.rental_announcement.serializers import (
    BookingCreateSerializer,
    ApprovedBookingSerializer,
    BookingRetrieveUpdateSerializer,
    CancelBookingSerializer,
    AllBookingsSerializer
)
from apps.users.permissions import IsRenter, IsLessor


class BookingListCreateAPIView(ListCreateAPIView):
    """
    View to list all bookings or create a new booking.

    Permissions:
        - `IsRenter` or `IsLessor`: Only renters or lessors can access this view.

    Methods:
        - `get_queryset`: Returns bookings based on user type.
        - `perform_create`: Sets the renter of the booking to the current user.
    """
    permission_classes = [IsRenter | IsLessor]
    serializer_class = BookingCreateSerializer

    def get_queryset(self):
        """
        Return bookings based on whether the user is a lessor or a renter.

        Returns:
            QuerySet: A queryset of bookings filtered by user role.
        """
        if self.request.user.is_lessor:
            return Booking.objects.filter(announcement__owner=self.request.user)
        return Booking.objects.filter(renter=self.request.user)

    def perform_create(self, serializer):
        """
        Save the booking with the current user as the renter.

        Args:
            serializer (serializers.ModelSerializer): The serializer instance.
        """
        serializer.save(renter=self.request.user)


class BookingRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific booking.

    Permissions:
        - `IsRenter` or `IsLessor`: Only renters or lessors can access this view.

    Methods:
        - `get_queryset`: Returns bookings for the authenticated user.
        - `get_object`: Retrieves the booking instance or returns 404 if not found.
        - `perform_update`: Updates the booking instance with the current user as the renter.
    """
    permission_classes = [IsRenter | IsLessor]
    serializer_class = BookingRetrieveUpdateSerializer

    def get_queryset(self):
        """
        Return bookings for the authenticated user.

        Returns:
            QuerySet: A queryset of bookings for the current user.
        """
        if self.request.user.is_authenticated:
            return Booking.objects.filter(renter=self.request.user)
        return Booking.objects.none()

    def get_object(self):
        """
        Retrieve the booking instance by primary key.

        Returns:
            Booking: The booking instance with the given primary key.

        Raises:
            Http404: If no booking is found with the given primary key.
        """
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        """
        Update the booking with the current user as the renter.

        Args:
            serializer (serializers.ModelSerializer): The serializer instance.
        """
        serializer.save(renter=self.request.user)


class BookingApproveAPIView(UpdateAPIView):
    """
    View to approve a booking.

    Permissions:
        - `IsAuthenticated` and `IsLessor`: Only authenticated users with the 'lessor' role can approve bookings.

    Methods:
        - `get_queryset`: Returns bookings owned by the lessor.
        - `perform_update`: Updates the booking status to 'Approved' if validated.
        - `update`: Handles the update request and returns the updated booking data.
    """
    permission_classes = [IsAuthenticated & IsLessor]
    serializer_class = ApprovedBookingSerializer

    def get_queryset(self):
        """
        Return bookings for the authenticated lessor.

        Returns:
            QuerySet: A queryset of bookings owned by the lessor.
        """
        if self.request.user.is_authenticated and self.request.user.is_lessor:
            return Booking.objects.filter(announcement__owner=self.request.user)
        return Booking.objects.none()

    def perform_update(self, serializer):
        """
        Update the booking status to 'Approved' if validated.

        Args:
            serializer (serializers.ModelSerializer): The serializer instance.
        """
        if serializer.validated_data.get('is_approved'):
            serializer.save(status=BookingStatus.APPROVED.value)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Handle the update request and return the updated booking data.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object with updated booking data.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class BookingCancelAPIView(UpdateAPIView):
    """
    View to cancel a booking.

    Permissions:
        - `IsAuthenticated`, `IsRenter`, or `IsLessor`: Authenticated users, renters, or lessors can cancel bookings.

    Methods:
        - `get_queryset`: Returns bookings for the authenticated user.
        - `perform_update`: Updates the booking status to 'Cancelled' if validated.
        - `update`: Handles the update request and returns the updated booking data.
    """
    permission_classes = [IsAuthenticated | IsRenter | IsLessor]
    serializer_class = CancelBookingSerializer

    def get_queryset(self):
        """
        Return bookings for the authenticated user.

        Returns:
            QuerySet: A queryset of bookings for the current user.
        """
        if self.request.user.is_authenticated:
            return Booking.objects.filter(renter=self.request.user)
        return Booking.objects.none()

    def perform_update(self, serializer):
        """
        Update the booking status to 'Cancelled' if validated.

        Args:
            serializer (serializers.ModelSerializer): The serializer instance.
        """
        if serializer.validated_data.get('canceled'):
            serializer.save(status=BookingStatus.CANCELLED.value)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Handle the update request and return the updated booking data.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object with updated booking data.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class AllBookingsAPIView(ListAPIView):
    """
    View to list all bookings for the authenticated user.

    Permissions:
        - `IsAuthenticated` or `IsRenter`: Authenticated users or renters can view their bookings.

    Methods:
        - `get_queryset`: Returns bookings for the authenticated user.
    """
    permission_classes = [IsAuthenticated | IsRenter]
    serializer_class = AllBookingsSerializer

    def get_queryset(self):
        """
        Return bookings for the authenticated user.

        Returns:
            QuerySet: A queryset of bookings for the current user.
        """
        if self.request.user.is_authenticated:
            return Booking.objects.filter(renter=self.request.user)

        return Booking.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Return a list of bookings for the authenticated user.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object with a list of bookings or a message if no bookings are found.
        """
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response(
            {'message': 'You have no reservations.'},
            status=status.HTTP_200_OK
        )
