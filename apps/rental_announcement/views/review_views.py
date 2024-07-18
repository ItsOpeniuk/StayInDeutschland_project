from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.rental_announcement.serializers import ReviewCreateSerializer
from apps.rental_announcement.serializers.review_list_serializer import ReviewListSerializer
from apps.rental_announcement.models import Review
from apps.users.permissions import IsRenter, IsLessor


class ReviewListCreateAPIView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated | IsRenter | IsLessor]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated | IsRenter | IsLessor]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Review.objects.filter(user=self.request.user)

        return Review.objects.none()

    def get_object(self):
        return get_object_or_404(Review, pk=self.kwargs['pk'])
