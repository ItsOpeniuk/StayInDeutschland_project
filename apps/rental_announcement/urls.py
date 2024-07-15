from django.urls import path

from apps.rental_announcement.views import CreateAddressView

urlpatterns = [
    path('create_address/', CreateAddressView.as_view(), name='create_address'),
]