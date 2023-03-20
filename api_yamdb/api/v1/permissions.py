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
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.role == User.Role.admin:
            return True


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if not bool(request.user and request.user.is_authenticated):
#             return False
#         if request.method == 'POST':
#             return True
#         if (request.user.role == User.Role.admin
#                 or request.user.role == User.Role.moderator):
#             return True
#
#     def has_object_permission(self, request, view, obj):
#         return obj.author == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == User.Role.admin
                or request.user.role == User.Role.moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
