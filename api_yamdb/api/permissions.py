from rest_framework import permissions


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Разрешения только для Администратора, Модератора, Автора.
    Для остальных только чтение"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)


class IsAdmin(permissions.BasePermission):
    """Рарзрешение только для Администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class IsAdminOrSuperUserOrReadOnly(permissions.BasePermission):
    """Разрешение только для Администратора и СуперЮзера."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))
