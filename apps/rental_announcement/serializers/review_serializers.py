from rest_framework import serializers
from apps.rental_announcement.models import Review, Booking
from apps.rental_announcement.choices.booking_status import BookingStatus


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['announcement', 'message', 'grade']

    def validate(self, data):
        user = self.context['request'].user
        announcement = data['announcement']

        has_approved_booking = Booking.objects.filter(
            renter=user,
            announcement=announcement,
            status=BookingStatus.APPROVED
        ).exists()

        if not has_approved_booking:
            raise serializers.ValidationError("You must have an approved booking to leave a review.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Review.objects.create(user=user, **validated_data)
