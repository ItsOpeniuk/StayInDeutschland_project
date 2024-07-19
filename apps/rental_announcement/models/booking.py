from django.db import models

from apps.rental_announcement.choices.booking_status import BookingStatus
from apps.users.models import User

class Booking(models.Model):
    """
    Model representing a booking for a rental announcement.

    Attributes:
        renter (User): The user who made the booking.
        announcement (Announcement): The announcement that was booked.
        start_date (date): The start date of the booking.
        end_date (date): The end date of the booking.
        status (str): The status of the booking (e.g., pending, approved, cancelled).
        is_approved (bool): Indicates if the booking has been approved.
        canceled (bool): Indicates if the booking has been cancelled.
        created_at (datetime): The date and time when the booking was created.
        updated_at (datetime): The date and time when the booking was last updated.
        deleted_at (datetime): The date and time when the booking was deleted, if applicable.
    """
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=BookingStatus.choices(), default=BookingStatus.PENDING.value)
    is_approved = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
