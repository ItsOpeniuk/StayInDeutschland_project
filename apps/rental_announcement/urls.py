from django.urls import path

from apps.rental_announcement.views import AddressListView, AddressRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('addresses/', AddressListView.as_view(), name='create_address'),
    path('update-address/<int:pk>/', AddressRetrieveUpdateDestroyAPIView.as_view(), name='update_address'),
]
