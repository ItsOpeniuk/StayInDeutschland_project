from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRenterOrReadOnly(BasePermission):


    def has_permission(self, request, view):

        return request.user.is_authenticated and  not request.user.is_lessor

    def has_object_permission(self, request, view, obj):

        return obj.renter == request.user
