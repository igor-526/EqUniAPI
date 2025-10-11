from django.contrib.auth.models import Group


def set_user_groups():
    Group.objects.get_or_create(name="UserAdmin")
    Group.objects.get_or_create(name="HorseModerator")
    Group.objects.get_or_create(name="GalleryModerator")
    Group.objects.get_or_create(name="ServiceModerator")
    Group.objects.get_or_create(name="EquestrianAdministrator")
