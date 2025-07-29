from rest_framework import permissions


class HorsePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user and request.user.is_authenticated():
            return False
        return bool('horses.change_horse' in
                    request.user.get_group_permissions())


class HorsePedigreePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user and request.user.is_authenticated():
            return False
        return bool('horses.change_horse' in
                    request.user.get_group_permissions())
