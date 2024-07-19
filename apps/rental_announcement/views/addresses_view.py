from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from apps.rental_announcement.models import Address
from apps.rental_announcement.serializers import DetailAddressSerializer
from apps.users.permissions import IsLessor


class AddressListView(ListCreateAPIView):
    """
    View to list all addresses or create a new address.

    Permissions:
        - `IsLessor`: Only users with the 'lessor' role can access this view.

    Methods:
        - `get_queryset`: Returns all addresses if the user is a lessor, otherwise returns an empty queryset.
        - `post`: Handles the creation of a new address.
    """
    permission_classes = [IsLessor]
    serializer_class = DetailAddressSerializer

    def get_queryset(self):
        """
        Return the list of addresses for lessors only.

        Returns:
            QuerySet: A queryset of all addresses for lessors or an empty queryset for non-lessors.
        """
        user = self.request.user
        if user.is_lessor:
            return Address.objects.all()
        return Address.objects.none()

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle the creation of a new address.

        Args:
            request (Request): The HTTP request object containing address data.

        Returns:
            Response: A response object with the status and the created address data or errors.
        """
        if not self.request.user.is_authenticated or not self.request.user.is_lessor:
            return Response(
                {"message": "You must be logged in as a lessor to create an address."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AddressRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific address.

    Permissions:
        - `IsLessor`: Only users with the 'lessor' role can access this view.

    Methods:
        - `get_object`: Retrieves the address instance by primary key or returns a 404 error if not found.
    """
    queryset = Address.objects.all()
    permission_classes = [IsLessor]
    serializer_class = DetailAddressSerializer

    def get_object(self):
        """
        Retrieve the address instance by primary key.

        Returns:
            Address: The address instance with the given primary key.

        Raises:
            Http404: If no address is found with the given primary key.
        """
        return get_object_or_404(Address, pk=self.kwargs['pk'])
