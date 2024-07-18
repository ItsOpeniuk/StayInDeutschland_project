from enum import Enum


class HousingTypes(Enum):
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
        return [(attr.value, attr.value) for attr in cls]
    