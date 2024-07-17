from django.urls import path

from apps.rental_announcement.views import (
    AddressListView,
    AddressRetrieveUpdateDestroyAPIView,
    AnnouncementListCreateAPIView,
    AnnouncementRetrieveUpdateDestroyAPIView,
    BookingListCreateAPIView
)


urlpatterns = [
    path('addresses/', AddressListView.as_view(), name='create_address'),
    path('address/<int:pk>/', AddressRetrieveUpdateDestroyAPIView.as_view(), name='update_address'),
    path('announcement/', AnnouncementListCreateAPIView.as_view(), name='create_announcement'),
    path('announcement/<int:pk>/', AnnouncementRetrieveUpdateDestroyAPIView.as_view(), name='update_announcement'),
    path('booking/', BookingListCreateAPIView.as_view(), name='create_booking'),
]
