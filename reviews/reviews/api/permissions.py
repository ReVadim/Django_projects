from rest_framework.permissions import BasePermission


class IsAdminPermission(BasePermission):
    """ Simple Base Permission class """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        return request.user.is_authenticated and request.user.is_superuser
