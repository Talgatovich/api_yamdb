from rest_framework import permissions


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """
    Права доступа для изменения файла
    автора, администратора и модератора.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class AdminOrReadOnly(permissions.BasePermission):
    """
    Права доступа для изменения только у
    администратора, для всех остальных чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role.admin
        )
