from datetime import timedelta

from django.db.models import Q
from rest_framework import serializers
from django.utils import timezone
from apps.rental_announcement.models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['renter', 'announcement', 'start_date', 'end_date']
        read_only_fields = ['renter']

    def validate_start_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'Start date cannot be in the past.'
            )
        return value

    def validate_end_date(self, value):
        if value < timezone.now().date() + timedelta(days=1):
            raise serializers.ValidationError(
                'End date should be more than today.'
            )
        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        announcement = data.get('announcement')

        if not announcement.is_active:
            raise serializers.ValidationError(
                'This announcement is not active.'
            )

        if end_date <= start_date:
            raise serializers.ValidationError(
                'End date cannot be less than start date.'
            )

        bookings = (Booking.objects.filter(announcement=announcement, is_approved=True, canceled=False).
                    filter(Q(start_date__lte=end_date) & Q(end_date__gte=start_date)))

        if bookings.exists():
            raise serializers.ValidationError(
                'Booking for this dates is reserved.'
            )

        return data
