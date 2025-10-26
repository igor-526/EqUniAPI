from typing import ClassVar
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import NewUser
from django.contrib.auth.models import Group


class UserNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["first_name", "last_name", "patronymic"]


class UserSelfSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = NewUser
        fields = [
            "first_name",
            "last_name",
            "patronymic",
            "photo",
            "groups",
        ]

    def get_groups(self, obj) -> list[str]:
        return list(obj.groups.all().values_list("name", flat=True))


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        validators=[UniqueValidator(queryset=NewUser.objects.all())],
    )

    class Meta:
        model = NewUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "username",
            "email",
            "photo",
            "password",
            "groups",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "username": {"required": True},
            "photo": {"read_only": True},
            "groups": {"required": False},
        }

    def create(self, validated_data: dict):
        password = validated_data.pop("password")
        groups = validated_data.pop("groups", [])
        user = NewUser(**validated_data)
        user.set_password(password)
        user.save()

        if groups:
            user.groups.set(groups)

        return user
    
    def update(self, instance: NewUser, validated_data: dict):
        password = validated_data.get("password", None)
        groups = validated_data.get("groups", None)

        if password:
            instance.set_password(password)
            instance.save()

        if groups:
            instance.groups.set(groups)

        user = super().update(instance, validated_data)

        return user
    

class UserGroupsMetadataSerializer(serializers.ModelSerializer):
    _GROUPS_TRANSLATE_REGISTRY: ClassVar[dict[str, str]] = {
        "UserAdmin": "Администратор пользователей",
        "HorseModerator": "Модератор лошадей",
        "GalleryModerator": "Модератор галереи",
        "ServiceModerator": "Модератор услуг",
        "EquestrianAdministrator": "Администратор информации"
    }

    title = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id", "name", "title"
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"read_only": True},
        }

    def get_title(self, obj: Group):
        return self._GROUPS_TRANSLATE_REGISTRY.get(obj.name, obj.name)


class UserPageMetadataSerializer(serializers.Serializer):
    user_groups = UserGroupsMetadataSerializer(many=True, read_only=True)

    class Meta:
        fields = [
            "user_groups",
        ]