from django.db import models
from django.db.models import Avg

from apps.rental_announcement.choices.type_of_object import HousingTypes
from apps.users.models import User

class Announcement(models.Model):
    """
    Model representing a rental announcement.

    Attributes:
        title (str): The title of the announcement.
        description (str): The description of the announcement.
        owner (User): The user who owns the announcement.
        address (Address): The address associated with the announcement.
        price (Decimal): The price of the rental.
        rooms (int): The number of rooms in the rental.
        type_of_object (str): The type of housing (e.g., apartment, house).
        is_active (bool): Indicates if the announcement is active.
        created_at (datetime): The date and time when the announcement was created.
        updated_at (datetime): The date and time when the announcement was last updated.
        deleted (bool): Indicates if the announcement has been deleted.
    """
    title = models.CharField(max_length=50)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    address = models.ForeignKey(
        'rental_announcement.Address',
        on_delete=models.CASCADE,
        related_name='announcements'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.SmallIntegerField()
    type_of_object = models.CharField(max_length=50, choices=HousingTypes.choices())
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    @property
    def average_rating(self):
        """
        Calculates the average rating of the announcement based on its reviews.

        Returns:
            float: The average rating rounded to one decimal place. If there are no reviews, returns 0.
        """
        reviews = self.reviews.all()
        if reviews:
            avg_rate = sum(review.grade for review in reviews) / len(reviews)
            return round(avg_rate, 1)
        return 0
