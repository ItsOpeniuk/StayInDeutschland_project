from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(unique=True, max_length=30, validators=[MinLengthValidator(2)])
    name = models.CharField(max_length=25, validators=[MinLengthValidator(2)])
    surname = models.CharField(max_length=25, validators=[MinLengthValidator(2)])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_lessor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'surname', 'phone']

    def __str__(self):
        return f'{self.username} {self.phone}'

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']
