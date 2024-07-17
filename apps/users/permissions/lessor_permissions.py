from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLessor(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_authenticated and request.user.is_lessor

    def has_object_permission(self, request, view, obj):

        return obj.announcement.owner == request.user
