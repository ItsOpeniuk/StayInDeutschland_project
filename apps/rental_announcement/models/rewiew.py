from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from apps.users.models import User


class Rewiew(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewiews')
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='rewiews')
    message = models.TextField(validators=[MinLengthValidator(20)])
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rewiews'
        ordering = ['-created_at']
