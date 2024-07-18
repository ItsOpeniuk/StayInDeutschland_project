from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from apps.users.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='reviews')
    message = models.TextField(validators=[MinLengthValidator(20)])
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
