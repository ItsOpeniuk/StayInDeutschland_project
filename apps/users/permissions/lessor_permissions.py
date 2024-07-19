from rest_framework.permissions import BasePermission


class IsLessor(BasePermission):
    """
    Custom permission class to grant access only to lessors.

    This permission class is used to restrict access to views based on whether
    the user is a lessor. It checks both general permissions for the view
    and object-specific permissions if required.

    Methods:
        has_permission(request, view):
            Checks if the user has permission to access the view.

        has_object_permission(request, view, obj):
            Checks if the user has permission to access a specific object.

    Permissions:
        - has_permission: Grants access if the user is authenticated and is a lessor.
        - has_object_permission: Grants access if the user is the owner of the announcement related to the object.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and is a lessor.

        Args:
            request (Request): The request object.
            view (View): The view object being accessed.

        Returns:
            bool: True if the user is authenticated and is a lessor, otherwise False.
        """
        return request.user.is_authenticated and request.user.is_lessor

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the specific object.

        Args:
            request (Request): The request object.
            view (View): The view object being accessed.
            obj (Model): The object being accessed.

        Returns:
            bool: True if the user is the owner of the announcement related to the object, otherwise False.
        """
        return obj.announcement.owner == request.user
