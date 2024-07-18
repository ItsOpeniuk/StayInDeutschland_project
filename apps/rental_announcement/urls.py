from django.urls import path

from apps.rental_announcement.views import (
    AddressListView,
    AddressRetrieveUpdateDestroyAPIView,
    AnnouncementListCreateAPIView,
    AnnouncementRetrieveUpdateDestroyAPIView,
    BookingListCreateAPIView,
    BookingRetrieveUpdateDestroyAPIView,
    BookingApproveAPIView,
    BookingCancelAPIView,
    AllBookingsAPIView,
    ReviewListCreateAPIView,
    ReviewRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('addresses/', AddressListView.as_view(), name='create_address'),
    path('address/<int:pk>/', AddressRetrieveUpdateDestroyAPIView.as_view(), name='update_address'),
    path('announcement/', AnnouncementListCreateAPIView.as_view(), name='create_announcement'),
    path('announcement/<int:pk>/', AnnouncementRetrieveUpdateDestroyAPIView.as_view(), name='update_announcement'),
    path('booking/', BookingListCreateAPIView.as_view(), name='create_booking'),
    path('booking/<int:pk>/', BookingRetrieveUpdateDestroyAPIView.as_view(), name='update_booking'),
    path('booking/approve/<int:pk>/', BookingApproveAPIView.as_view(), name='approve_booking'),
    path('booking/canceled/<int:pk>/', BookingCancelAPIView.as_view(), name='cancel_booking'),
    path('booking/history/', AllBookingsAPIView.as_view(), name='all_bookings'),
    path('review/', ReviewListCreateAPIView.as_view(), name='create_review'),
    path('review/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='update_review'),
]
