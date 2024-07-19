from enum import Enum

class BookingStatus(Enum):
    """
    Enumeration for different booking statuses.
    """
    PENDING = 'Pending'
    APPROVED = 'Approved'
    CANCELLED = 'Cancelled'

    @classmethod
    def choices(cls):
        """
        Provides choices for the booking status enumeration.

        Returns:
            list: A list of tuples where each tuple contains the value and the value of the booking status.
        """
        return [(key.value, key.value) for key in cls]
