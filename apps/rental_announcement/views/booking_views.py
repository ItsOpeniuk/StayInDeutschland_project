from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    get_object_or_404, ListAPIView)
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

    permission_classes = [IsRenter | IsLessor]
    serializer_class = BookingCreateSerializer

    def get_queryset(self):
        if self.request.user.is_lessor:
            return Booking.objects.filter(announcement__owner=self.request.user)

        return Booking.objects.filter(renter=self.request.user)

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)


class BookingRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsRenter | IsLessor]
    serializer_class = BookingRetrieveUpdateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Booking.objects.filter(renter=self.request.user)
        return Booking.objects.none()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        serializer.save(renter=self.request.user)


class BookingApproveAPIView(UpdateAPIView):

    permission_classes = [IsAuthenticated | IsLessor]
    serializer_class = ApprovedBookingSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_lessor:
            return Booking.objects.filter(announcement__owner=self.request.user)
        return Booking.objects.none()

    def perform_update(self, serializer):
        if serializer.validated_data.get('is_approved'):
            serializer.save(status=BookingStatus.APPROVED.value)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
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

    permission_classes = [IsAuthenticated | IsRenter | IsLessor]
    serializer_class = CancelBookingSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Booking.objects.filter(renter=self.request.user)

        return Booking.objects.none()

    def perform_update(self, serializer):
        if serializer.validated_data.get('canceled'):
            serializer.save(status=BookingStatus.CANCELLED.value)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
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

    permission_classes = [IsAuthenticated | IsRenter]
    serializer_class = AllBookingsSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Booking.objects.filter(renter=self.request.user)


        return Response(
            {'message': 'You have no reservations.'},
            status=status.HTTP_200_OK
        )