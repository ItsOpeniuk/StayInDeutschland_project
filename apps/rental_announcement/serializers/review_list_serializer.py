from rest_framework import serializers
from apps.rental_announcement.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing reviews.

    Includes:
        - `user`: A string representation of the user who wrote the review (read-only).
        - `announcement`: A string representation of the announcement being reviewed (read-only).
        - `message`: The content of the review message.
        - `grade`: The rating grade given in the review.

    Meta:
        model (Review): The model to be serialized.
        fields (list): The fields to include in the serialized representation.
        read_only_fields (list): The fields that are read-only.
    """
    user = serializers.StringRelatedField(read_only=True)
    announcement = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['user', 'announcement', 'message', 'grade']
        read_only_fields = ['user', 'announcement']
