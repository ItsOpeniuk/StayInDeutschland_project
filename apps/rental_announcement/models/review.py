from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from apps.users.models import User

class Review(models.Model):
    """
    Model representing a review for a rental announcement.

    Attributes:
        user (User): The user who wrote the review.
        announcement (Announcement): The announcement being reviewed.
        message (str): The text content of the review. Must be at least 20 characters long.
        grade (int): The rating given in the review. Must be between 1 and 5.
        created_at (datetime): The date and time when the review was created.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='reviews')
    message = models.TextField(validators=[MinLengthValidator(20)])
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
