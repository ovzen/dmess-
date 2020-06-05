"""
Специальные разрешения для использования в представлениях (view)
"""

from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    """
    Custom permission to allow admins all permissions and
    only safe methods to all others
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
