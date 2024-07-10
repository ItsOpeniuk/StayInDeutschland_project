from django.db import models

from apps.rental_announcement.choices.booking_status import BookingStatus


class Booking(models.Model):
    renter = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bookings')
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=BookingStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
