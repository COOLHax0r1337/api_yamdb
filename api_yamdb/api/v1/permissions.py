from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdminOrMe(permissions.BasePermission):
    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if view.kwargs.get('username') == 'me':
            return True
        if request.user.role == User.Role.admin:
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role == User.Role.admin:
            return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role == (User.Role.admin or User.Role.moderator):
            return True
        if bool(request.user
                and request.user.is_authenticated
                and request.method == 'POST'
                ):
            return True
        return obj.author == request.user
