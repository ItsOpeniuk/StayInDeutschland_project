import django_filters
from apps.rental_announcement.models import Announcement

class AnnouncementFilter(django_filters.FilterSet):
    """
    FilterSet for filtering announcements based on various fields.
    """

    class Meta:
        model = Announcement
        fields = {
            'rooms': ['gte', 'lte'],
            'price': ['gte', 'lte'],
            'type_of_object': ['exact'],
            'address__city': ['exact', 'icontains'],
            'address__federal_land': ['exact'],
        }
