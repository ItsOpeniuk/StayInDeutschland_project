from datetime import timedelta

from django.db.models import Q
from rest_framework import serializers
from django.utils import timezone

from apps.rental_announcement.choices.booking_status import BookingStatus
from apps.rental_announcement.models import Booking
from apps.users.models import User


class BookingCreateSerializer(serializers.ModelSerializer):

    renter = serializers.SlugRelatedField('email', read_only=True)

    class Meta:
        model = Booking
        fields = ['renter', 'announcement', 'status', 'start_date', 'end_date']
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


class BookingRetrieveUpdateSerializer(serializers.ModelSerializer):

    renter = serializers.StringRelatedField(read_only=True)

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
        instance = self.instance
        start_date = data.get('start_date', instance.start_date)
        end_date = data.get('end_date', instance.end_date)
        announcement = data.get('announcement', instance.announcement)

        if not announcement.is_active:
            raise serializers.ValidationError(
                'This announcement is not active.'
            )

        if end_date <= start_date:
            raise serializers.ValidationError(
                'End date cannot be less than start date.'
            )

        bookings = (Booking.objects.filter(announcement=announcement, is_approved=True, canceled=False).
                    filter(Q(start_date__lte=end_date) & Q(end_date__gte=start_date)).
                    exclude(id=instance.id))

        if bookings.exists():
            raise serializers.ValidationError(
                'Booking for this dates is reserved.'
            )

        return data


class ApprovedBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['is_approved']

    def update(self, instance, validated_data):
        if validated_data.get('is_approved'):
            validated_data['status'] = BookingStatus.APPROVED.value

        return super().update(instance, validated_data)

class CancelBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['canceled']


    def update(self, instance, validated_data):
        if validated_data.get('canceled'):
            validated_data['status'] = BookingStatus.CANCELLED.value
            validated_data['is_approved'] = False

        return super().update(instance, validated_data)


class AllBookingsSerializer(serializers.ModelSerializer):

    Lessor = serializers.StringRelatedField(read_only=True)
    announcement = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['Lessor', 'announcement', 'start_date', 'end_date', 'status']
        ordering = ['-created_at']
