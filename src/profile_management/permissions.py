from rest_framework import permissions

from profile_management.models import NewUser


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user and request.user.is_authenticated():
            return False
        return get_has_users_admin_permission(request.user)


def get_has_users_admin_permission(user: NewUser):
    return bool(user.groups.filter(name="UserAdmin").exists())
