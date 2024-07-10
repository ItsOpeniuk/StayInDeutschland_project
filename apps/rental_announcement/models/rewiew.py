from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


class Rewiew(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rewiews')
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='rewiews')
    message = models.TextField(validators=MinLengthValidator(20))
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

