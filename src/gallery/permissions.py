from profile_management.models import NewUser

from rest_framework import permissions


class GalleryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user and request.user.is_authenticated():
            return False
        return get_has_gallery_moderate_permission(request.user)


def get_has_gallery_moderate_permission(user: NewUser):
    return bool(user.has_perm("gallery.change_photo"))
