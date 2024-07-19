from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission class to grant access only to the owner of the object.

    This permission class ensures that the user making the request is the owner
    of the object they are trying to access. It is commonly used to enforce object-level
    permissions where only the creator or owner of an object is allowed to modify or view it.

    Methods:
        has_object_permission(request, view, obj):
            Checks if the user is the owner of the object.

    Permissions:
        - has_object_permission: Grants access if the user making the request is the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user making the request is the owner of the object.

        Args:
            request (Request): The request object.
            view (View): The view object being accessed.
            obj (Model): The object being accessed.

        Returns:
            bool: True if the user making the request is the owner of the object, otherwise False.
        """
        return obj == request.user
