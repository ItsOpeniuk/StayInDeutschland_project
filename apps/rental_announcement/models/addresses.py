from django.db import models
from apps.rental_announcement.choices.federal_lands import FederalLands

class Address(models.Model):
    """
    Model representing an address.

    Attributes:
        federal_land (str): The federal state where the address is located.
        city (str): The city of the address.
        street (str): The street of the address.
        house_number (str): The house number of the address.
        postal_code (str): The postal code of the address.
    """
    federal_land = models.CharField(max_length=50, choices=FederalLands.choices())
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=75)
    house_number = models.CharField(max_length=5)
    postal_code = models.CharField(max_length=5)

    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        unique_together = ['federal_land', 'city', 'street', 'house_number', 'postal_code']

    def __str__(self):
        return f"{self.street}, {self.house_number}, {self.postal_code}, {self.city}"
