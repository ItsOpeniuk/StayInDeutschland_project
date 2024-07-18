from django.db import models

from apps.rental_announcement.choices.type_of_object import HousingTypes
from apps.rental_announcement.abstract_models.abstract_models import SoftDeleteAnnouncementModel
from apps.users.models import User


# class AnnouncementManager(models.Manager):
#
#     def get_queryset(self):
#         return super().get_queryset().filter(is_active=True, is_deleted=False)


class Announcement(models.Model):
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

    # objects = AnnouncementManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'


    @property
    def average_rate(self):
        return self.rewiews.agregate(awg_rate='rate')['awg_rate']
