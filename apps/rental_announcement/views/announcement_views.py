from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.users.permissions.lessor_permissions import IsLessor
from apps.rental_announcement.models import Announcement
from apps.rental_announcement.filters import AnnouncementFilter
from apps.rental_announcement.serializers import (
    AnnouncementRetrieveUpdateDestroySerializer,
    AnnouncementListDetailSerializer,
)


class AnnouncementListCreateAPIView(ListCreateAPIView):
    """
    View to list all announcements or create a new announcement.

    Permissions:
        - `IsAuthenticated`: Only authenticated users can access this view.
        - `IsLessor`: Only users with the 'lessor' role can create announcements.

    Filtering:
        - `DjangoFilterBackend`: Allows filtering using DjangoFilter.
        - `SearchFilter`: Allows searching by `title` and `description`.
        - `OrderingFilter`: Allows ordering by `price` and `created_at`.

    Methods:
        - `get_serializer_class`: Chooses the serializer class based on the HTTP method.
        - `get_permissions`: Returns permissions based on the HTTP method.
    """
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AnnouncementFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAuthenticated, IsLessor]
    # queryset = Announcement.objects.all()

    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the HTTP method.

        Returns:
            Type: Serializer class for the request method.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AnnouncementRetrieveUpdateDestroySerializer
        return AnnouncementListDetailSerializer

    def get_permissions(self):
        """
        Return the appropriate permissions based on the HTTP method.

        Returns:
            List: A list of permission classes for the request method.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return [IsLessor()]
        return [IsAuthenticated()]


class AnnouncementRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific announcement.

    Permissions:
        - `IsAuthenticated`: Only authenticated users can access this view.
        - `IsLessor`: Only users with the 'lessor' role can access this view.

    Methods:
        - `get_queryset`: Returns announcements owned by the authenticated lessor.
        - `get_object`: Retrieves the announcement instance by primary key or returns a 404 error if not found.
    """
    permission_classes = [IsAuthenticated, IsLessor]
    serializer_class = AnnouncementRetrieveUpdateDestroySerializer

    def get_queryset(self):
        """
        Return announcements owned by the authenticated user if they are a lessor.

        Returns:
            QuerySet: A queryset of announcements owned by the user or an empty queryset.
        """
        if self.request.user.is_authenticated and self.request.user.is_lessor:
            return Announcement.objects.filter(owner=self.request.user)
        return Announcement.objects.none()

    def get_object(self):
        """
        Retrieve the announcement instance by primary key.

        Returns:
            Announcement: The announcement instance with the given primary key.

        Raises:
            Http404: If no announcement is found with the given primary key.
        """
        return get_object_or_404(Announcement, pk=self.kwargs['pk'])
