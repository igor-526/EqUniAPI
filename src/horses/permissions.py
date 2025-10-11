from rest_framework import permissions

from profile_management.models import NewUser


class HorsePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user and request.user.is_authenticated():
            return False
        return get_has_horses_moderate_permission(request.user)


def get_has_horses_moderate_permission(user: NewUser):
    return bool(user.has_perm("horses.change_horse"))
