from rest_framework import serializers

from apps.rental_announcement.models.addresses import Address

class DetailAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the Address model, including all fields.

    This serializer is used to convert Address model instances into JSON format
    and validate incoming data for Address model instances.

    Meta:
        model (Address): The model to be serialized.
        fields (list): The fields to include in the serialized representation.
    """
    class Meta:
        model = Address
        fields = '__all__'
