from rest_framework import serializers

from apps.rental_announcement.models import Announcement, Address
from apps.rental_announcement.serializers import DetailAddressSerializer
from apps.rental_announcement.serializers.review_list_serializer import ReviewListSerializer


class AnnouncementListDetailSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only=True)
    address = serializers.StringRelatedField(read_only=True)
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating

    class Meta:
        model = Announcement
        exclude = ['updated_at', 'deleted']


class AnnouncementRetrieveUpdateDestroySerializer(serializers.ModelSerializer):

    # owner = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    address = DetailAddressSerializer()
    reviews = ReviewListSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating

    class Meta:
        model = Announcement
        exclude = ['updated_at', 'deleted', 'is_active']

    def create(self, validated_data):
        raw_address_data = validated_data.pop('address')
        address, _ = Address.objects.get_or_create(**raw_address_data)
        return Announcement.objects.create(address=address, **validated_data)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address, _ = Address.objects.update_or_create(defaults=address_data, **address_data)
            instance.address = address

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
