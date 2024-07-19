from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractBaseUser and PermissionsMixin.

    Attributes:
        username (CharField): Unique username for the user. Must be at least 2 characters long.
        name (CharField): First name of the user. Must be at least 2 characters long.
        surname (CharField): Last name of the user. Must be at least 2 characters long.
        email (EmailField): Unique email address for the user.
        phone (CharField): Unique phone number for the user (optional).
        is_lessor (BooleanField): Flag indicating whether the user is a lessor.
        is_active (BooleanField): Flag indicating whether the user's account is active.
        is_staff (BooleanField): Flag indicating whether the user has staff (admin) rights.
        date_joined (DateTimeField): The date and time when the user registered.
        updated_at (DateTimeField): The date and time when the user was last updated.
        deleted_at (DateTimeField): The date and time when the user was soft-deleted (if applicable).
        deleted (BooleanField): Flag indicating whether the user is marked as deleted (soft delete).

    Manager:
        objects (UserManager): Manager for this model used for handling user operations.

    Meta:
        db_table (str): The name of the database table for the model.
        verbose_name (str): The singular name of the model.
        verbose_name_plural (str): The plural name of the model.
        ordering (list): The default ordering for the model's records (by descending date_joined).

    Methods:
        __str__(): Returns a string representation of the user, including name and phone number.
    """

    username = models.CharField(
        unique=True,
        max_length=30,
        validators=[MinLengthValidator(2)],
        help_text='Unique username for the user, must be at least 2 characters long.'
    )
    name = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(2)],
        help_text='First name of the user, must be at least 2 characters long.'
    )
    surname = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(2)],
        help_text='Last name of the user, must be at least 2 characters long.'
    )
    email = models.EmailField(
        unique=True,
        help_text='Unique email address for the user.'
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text='Unique phone number for the user (optional).'
    )
    is_lessor = models.BooleanField(
        default=False,
        help_text='Flag indicating whether the user is a lessor.'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Flag indicating whether the user\'s account is active.'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Flag indicating whether the user has staff (admin) rights.'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text='The date and time when the user registered.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='The date and time when the user was last updated.'
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='The date and time when the user was soft-deleted (if applicable).'
    )
    deleted = models.BooleanField(
        default=False,
        help_text='Flag indicating whether the user is marked as deleted (soft delete).'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'surname', 'phone']

    def __str__(self):
        """
        Returns a string representation of the user, including name and phone number.

        Returns:
            str: String representation of the user in the format "name surname | phone".
        """
        return f'{self.name} {self.surname} | {self.phone}'

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']
