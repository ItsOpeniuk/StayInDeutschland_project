from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


from apps.rental_announcement.models import Booking
from apps.rental_announcement.serializers import BookingCreateSerializer
from apps.users.permissions import IsRenterOrReadOnly, IsLessor


class BookingListCreateAPIView(ListCreateAPIView):

    permission_classes = [IsRenterOrReadOnly | IsLessor]
    serializer_class = BookingCreateSerializer

    def get_queryset(self):
        if self.request.user.is_lessor:
            return Booking.objects.filter(announcement__owner=self.request.user)

        return Booking.objects.filter(renter=self.request.user)

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)



