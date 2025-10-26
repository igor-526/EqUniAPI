from rest_framework import permissions

from profile_management.models import NewUser


class StaticInformationAdminPermission(permissions.BasePermission):
    message = "Недостаточно прав для выполнения действия."

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return is_equestrian_administrator(request.user)


def is_equestrian_administrator(user: NewUser | None) -> bool:
    if not user or not getattr(user, "is_authenticated", False):
        return False
    return bool(user.groups.filter(name="EquestrianAdministrator").exists())
