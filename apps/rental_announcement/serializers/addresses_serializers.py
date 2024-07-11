from rest_framework import serializers

from apps.rental_announcement.models.addresses import ObjectAddress


class CreateDetailAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjectAddress
        fields = '__all__'
