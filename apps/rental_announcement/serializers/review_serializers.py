from rest_framework import serializers
from apps.rental_announcement.models import Review, Booking
from apps.rental_announcement.choices.booking_status import BookingStatus


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating reviews.

    Includes:
        - `announcement`: The announcement being reviewed.
        - `message`: The content of the review message.
        - `grade`: The rating grade given in the review.

    Meta:
        model (Review): The model to be serialized.
        fields (list): The fields to include in the serialized representation.
    """
    class Meta:
        model = Review
        fields = ['announcement', 'message', 'grade']

    def validate(self, data):
        """
        Validates the review data to ensure the user has an approved booking for the announcement.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the user does not have an approved booking for the announcement.
        """
        user = self.context['request'].user
        announcement = data['announcement']

        has_approved_booking = Booking.objects.filter(
            renter=user,
            announcement=announcement,
            status=BookingStatus.APPROVED.value
        ).exists()

        if not has_approved_booking:
            raise serializers.ValidationError(
                "You must have an approved booking to leave a review."
            )

        return data

    def create(self, validated_data):
        """
        Creates a new review instance with the validated data.

        Args:
            validated_data (dict): The validated data for the review.

        Returns:
            Review: The created review instance.
        """
        user = self.context['request'].user
        return Review.objects.create(user=user, **validated_data)
