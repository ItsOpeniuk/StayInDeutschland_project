from rest_framework import serializers

from apps.rental_announcement.models import Announcement, Address
from apps.users.models import User
from apps.rental_announcement.serializers import DetailAddressSerializer


class AnnouncementListDetailSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only=True)
    address = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Announcement
        exclude = ['updated_at', 'deleted']


class AnnouncementRetrieveUpdateDestroySerializer(serializers.ModelSerializer):

    owner = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    address = DetailAddressSerializer()

    class Meta:
        model = Announcement
        exclude = ['updated_at', 'deleted']

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


# class AnnouncementSearchSerializer(serializers.Serializer):
#     keyword = serializers.CharField(required=False)
#     city = serializers.CharField(required=False)
#     min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
#     max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
#     sort_by = serializers.ChoiceField(choices=['price', 'created_at'], default='created_at')
#
#     def filter_queryset(self, queryset):
#         keyword = self.validated_data.get('keyword')
#         city = self.validated_data.get('city')
#         min_price = self.validated_data.get('min_price')
#         max_price = self.validated_data.get('max_price')
#         sort_by = self.validated_data.get('sort_by')
#
#         if keyword:
#             queryset = queryset.filter(description__icontains=keyword)
#
#         if city:
#             queryset = queryset.filter(city__icontains=city)
#
#         if min_price:
#             queryset = queryset.filter(price__gte=min_price)
#
#         if max_price:
#             queryset = queryset.filter(price__lte=max_price)
#
#         if sort_by == 'created_at':
#             queryset = queryset.order_by('-created_at')
#         elif sort_by == 'price':
#             queryset = queryset.order_by('price')
#
#         return queryset
