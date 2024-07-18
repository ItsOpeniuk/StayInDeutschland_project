from rest_framework.generics import (ListCreateAPIView,
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

    permission_classes = [IsLessor]
    serializer_class = DetailAddressSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_lessor:
            return Address.objects.all()
        return Address.objects.none()

    def post(self, request: Request, *args, **kwargs) -> Response:
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

    queryset = Address.objects.all()
    permission_classes = [IsLessor]
    serializer_class = DetailAddressSerializer

    def get_object(self):
        return get_object_or_404(Address, pk=self.kwargs['pk'])
