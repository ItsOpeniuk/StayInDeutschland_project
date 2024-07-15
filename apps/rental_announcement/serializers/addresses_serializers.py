from rest_framework import serializers

from apps.rental_announcement.models.addresses import Address


class CreateDetailAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'
