from rest_framework.permissions import BasePermission


class IsRenter(BasePermission):
    """
    Custom permission class to grant access only to renters.

    This permission class ensures that access is granted to users who are authenticated
    and are not marked as lessors. It is commonly used to enforce permissions where
    only renters are allowed to perform certain actions or access specific resources.

    Methods:
        has_permission(request, view):
            Checks if the user is authenticated and is not a lessor.

        has_object_permission(request, view, obj):
            Checks if the user making the request is the renter of the object.

    Permissions:
        - has_permission: Grants access if the user is authenticated and not a lessor.
        - has_object_permission: Grants access if the user making the request is the renter of the object.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and not a lessor.

        Args:
            request (Request): The request object.
            view (View): The view object being accessed.

        Returns:
            bool: True if the user is authenticated and is not a lessor, otherwise False.
        """
        return request.user.is_authenticated and not request.user.is_lessor

    def has_object_permission(self, request, view, obj):
        """
        Check if the user making the request is the renter of the object.

        Args:
            request (Request): The request object.
            view (View): The view object being accessed.
            obj (Model): The object being accessed.

        Returns:
            bool: True if the user making the request is the renter of the object, otherwise False.
        """
        return obj.user == request.user
