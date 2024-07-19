from enum import Enum

class HousingTypes(Enum):
    """
    Enumeration for different types of housing.
    """
    APARTMENT = "Apartment"
    HOUSE = "House"
    ROOM = "Room"
    STUDIO = "Studio"
    LOFT = "Loft"
    DUPLEX = "Duplex"
    TOWNHOUSE = "Townhouse"
    CONDO = "Condo"
    COTTAGE = "Cottage"
    VILLA = "Villa"
    PENTHOUSE = "Penthouse"
    HOTEL = "Hotel"
    HOSTEL = "Hostel"

    @classmethod
    def choices(cls):
        """
        Provides choices for the housing types enumeration.

        Returns:
            list: A list of tuples where each tuple contains the value and the value of the housing type.
        """
        return [(attr.value, attr.value) for attr in cls]
