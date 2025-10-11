from rest_framework import serializers

from .models import NewUser


class UserNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["first_name", "last_name", "patronymic"]


class UserSelfSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = NewUser
        fields = [
            "first_name",
            "last_name",
            "patronymic",
            "photo",
            "permissions",
            "groups",
        ]

    def get_groups(self, obj):
        return list(obj.groups.all().values_list("name", flat=True))

    def get_permissions(self, obj):
        return list(obj.get_group_permissions())
