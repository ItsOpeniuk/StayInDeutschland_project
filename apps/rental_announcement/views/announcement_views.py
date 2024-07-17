from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.users.permissions.lessor_permissions import IsLessor
from apps.rental_announcement.models import Announcement, Address
from apps.rental_announcement.filters import AnnouncementFilter
from apps.rental_announcement.serializers import (AnnouncementRetrieveUpdateDestroySerializer,
                                                  AnnouncementListDetailSerializer,
                                                  )



class AnnouncementListCreateAPIView(ListCreateAPIView):

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AnnouncementFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAuthenticated, IsLessor]
    queryset = Announcement.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AnnouncementRetrieveUpdateDestroySerializer

        return AnnouncementListDetailSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return [IsLessor()]
        return [IsAuthenticated()]


class AnnouncementRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    __model = Announcement
    permission_classes = [IsAuthenticated, IsLessor]
    serializer_class = AnnouncementRetrieveUpdateDestroySerializer

    def get_object(self):
        return get_object_or_404(self.__model, pk=self.kwargs['pk'])
