from rest_framework import serializers
from apps.rental_announcement.models import Review


class ReviewListSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    announcement = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['user', 'announcement', 'message', 'grade']
        read_only_fields = ['user', 'announcement']
