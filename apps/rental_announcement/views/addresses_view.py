from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from apps.rental_announcement.models import Address
from apps.rental_announcement.serializers import CreateDetailAddressSerializer

class CreateAddressView(CreateAPIView):
    serializer_class = CreateDetailAddressSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        user = self.request.user

        if not user.is_authenticated or not user.is_lessor:
            return Response(
                {"message": "You must be logged in to create an address and should be lessor"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CreateDetailAddressSerializer(data=request.data)
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
