from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.rental_announcement.serializers import ReviewCreateSerializer
from apps.rental_announcement.serializers.review_list_serializer import ReviewListSerializer
from apps.rental_announcement.models import Review
from apps.users.permissions import IsRenter, IsLessor


class ReviewListCreateAPIView(CreateAPIView):
    """
    View to create a new review.

    Permissions:
        - `IsAuthenticated` or `IsRenter` or `IsLessor`: Only authenticated users,
           renters, or lessors can create a review.

    Methods:
        - `get_queryset`: Returns reviews created by the current user.
        - `perform_create`: Sets the user of the review to the current user.
    """
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated | IsRenter | IsLessor]

    def get_queryset(self):
        """
        Return reviews created by the current user.

        Returns:
            QuerySet: A queryset of reviews created by the current user.
        """
        return Review.objects.filter(user=self.request.user)


class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific review.

    Permissions:
        - `IsAuthenticated` or `IsRenter` or `IsLessor`: Only authenticated users,
           renters, or lessors can access this view.

    Methods:
        - `get_queryset`: Returns reviews created by the current user.
        - `get_object`: Retrieves the review instance or returns 404 if not found.
    """
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated | IsRenter | IsLessor]

    def get_queryset(self):
        """
        Return reviews created by the current user.

        Returns:
            QuerySet: A queryset of reviews created by the current user.
        """
        if self.request.user.is_authenticated:
            return Review.objects.filter(user=self.request.user)
        return Review.objects.none()

    def get_object(self):
        """
        Retrieve the review instance by primary key.

        Returns:
            Review: The review instance with the given primary key.

        Raises:
            Http404: If no review is found with the given primary key.
        """
        return get_object_or_404(Review, pk=self.kwargs['pk'])
