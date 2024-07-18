from rest_framework import serializers

from apps.rental_announcement.models import Announcement, Address
from apps.users.models import User
from apps.rental_announcement.serializers import DetailAddressSerializer


class AnnouncementListDetailSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only=True)
    address = serializers.StringRelatedField(read_only=True)
    rating = serializers.FloatField(source='average_rating', read_only=True, default=5)

    class Meta:
        model = Announcement
        exclude = ['updated_at', 'deleted']


class AnnouncementRetrieveUpdateDestroySerializer(serializers.ModelSerializer):

    owner = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    address = DetailAddressSerializer()

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
