from datetime import timedelta

from django.db.models import Q
from rest_framework import serializers
from django.utils import timezone

from apps.rental_announcement.choices.booking_status import BookingStatus
from apps.rental_announcement.models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new bookings.

    Includes:
        - `renter`: The email of the user making the booking (read-only).
        - `announcement`: The announcement being booked.
        - `status`: The status of the booking.
        - `start_date`: The start date of the booking.
        - `end_date`: The end date of the booking.

    Meta:
        model (Booking): The model to be serialized.
        fields (list): The fields to include in the serialized representation.
        read_only_fields (list): The fields that are read-only.
    """
    renter = serializers.SlugRelatedField('email', read_only=True)

    class Meta:
        model = Booking
        fields = ['renter', 'announcement', 'start_date', 'end_date']
        read_only_fields = ['renter']

    def validate_start_date(self, value):
        """
        Validates the start date to ensure it is not in the past.

        Args:
            value (date): The start date of the booking.

        Returns:
            date: The validated start date.

        Raises:
            serializers.ValidationError: If the start date is in the past.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'Start date cannot be in the past.'
            )
        return value

    def validate_end_date(self, value):
        """
        Validates the end date to ensure it is at least one day after today.

        Args:
            value (date): The end date of the booking.

        Returns:
            date: The validated end date.

        Raises:
            serializers.ValidationError: If the end date is less than one day from today.
        """
        if value < timezone.now().date() + timedelta(days=1):
            raise serializers.ValidationError(
                'End date should be more than today.'
            )
        return value

    def validate(self, data):
        """
        Validates the booking data to ensure the booking does not overlap with existing bookings
        and the announcement is active.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If there are validation errors.
        """
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

        bookings = (Booking.objects.filter(announcement=announcement, is_approved=True, canceled=False)
                    .filter(Q(start_date__lte=end_date) & Q(end_date__gte=start_date)))

        if bookings.exists():
            raise serializers.ValidationError(
                'Booking for this dates is reserved.'
            )

        return data


class BookingRetrieveUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving, updating, and deleting bookings.

    Includes:
        - `renter`: A string representation of the user who made the booking (read-only).
        - `announcement`: The announcement being booked.
        - `start_date`: The start date of the booking.
        - `end_date`: The end date of the booking.

    Meta:
        model (Booking): The model to be serialized.
        fields (list): The fields to include in the serialized representation.
        read_only_fields (list): The fields that are read-only.
    """
    renter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['renter', 'announcement', 'start_date', 'end_date']
        read_only_fields = ['renter']

    def validate_start_date(self, value):
        """
        Validates the start date to ensure it is not in the past.

        Args:
            value (date): The start date of the booking.

        Returns:
            date: The validated start date.

        Raises:
            serializers.ValidationError: If the start date is in the past.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'Start date cannot be in the past.'
            )
        return value

    def validate_end_date(self, value):
        """
        Validates the end date to ensure it is at least one day after today.

        Args:
            value (date): The end date of the booking.

        Returns:
            date: The validated end date.

        Raises:
            serializers.ValidationError: If the end date is less than one day from today.
        """
        if value < timezone.now().date() + timedelta(days=1):
            raise serializers.ValidationError(
                'End date should be more than today.'
            )
        return value

    def validate(self, data):
        """
        Validates the updated booking data to ensure the booking does not overlap with existing bookings
        and the announcement is active.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If there are validation errors.
        """
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

        bookings = (Booking.objects.filter(announcement=announcement, is_approved=True, canceled=False)
                    .filter(Q(start_date__lte=end_date) & Q(end_date__gte=start_date))
                    .exclude(id=instance.id))

        if bookings.exists():
            raise serializers.ValidationError(
                'Booking for this dates is reserved.'
            )

        return data


class ApprovedBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the approval status of a booking.

    Includes:
        - `is_approved`: Indicates whether the booking is approved.

    Meta:
        model (Booking): The model to be serialized.
        fields (list): The fields to include in the serialized representation.
    """
    class Meta:
        model = Booking
        fields = ['is_approved']

    def update(self, instance, validated_data):
        """
        Updates the booking instance with the approved status.

        Args:
            instance (Booking): The booking instance to be updated.
            validated_data (dict): The validated data for updating the booking.

        Returns:
            Booking: The updated booking instance.
        """
        if validated_data.get('is_approved'):
            validated_data['status'] = BookingStatus.APPROVED.value

        return super().update(instance, validated_data)


class CancelBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the cancellation status of a booking.

    Includes:
        - `canceled`: Indicates whether the booking is canceled.

    Meta:
        model (Booking): The model to be serialized.
        fields (list): The fields to include in the serialized representation.
    """
    class Meta:
        model = Booking
        fields = ['canceled']

    def update(self, instance, validated_data):
        """
        Updates the booking instance with the canceled status.

        Args:
            instance (Booking): The booking instance to be updated.
            validated_data (dict): The validated data for updating the booking.

        Returns:
            Booking: The updated booking instance.
        """
        if validated_data.get('canceled'):
            validated_data['status'] = BookingStatus.CANCELLED.value
            validated_data['is_approved'] = False

        return super().update(instance, validated_data)


class AllBookingsSerializer(serializers.ModelSerializer):
    """
    Serializer for listing all bookings.

    Includes:
        - `Lessor`: A string representation of the lessor (user who made the booking).
        - `announcement`: A string representation of the announcement being booked.
        - `start_date`: The start date of the booking.
        - `end_date`: The end date of the booking.
        - `status`: The current status of the booking.

    Meta:
        model (Booking): The model to be serialized.
        fields (list): The fields to include in the serialized representation.
        ordering (list): The default ordering of the serialized data.
    """
    Lessor = serializers.StringRelatedField(read_only=True)
    announcement = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['Lessor', 'announcement', 'start_date', 'end_date', 'status']
        ordering = ['-created_at']
