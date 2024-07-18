from enum import Enum


class BookingStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    CANCELLED = 'Cancelled'

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]

    def __str__(self):
        return self.name
