from typing import Any

from django.core.exceptions import ValidationError
from rest_framework import serializers

from horses.validators import validate_phone_numbers
from .models import Contacts, ContactsGroups, KeyValueInformation

ALLOWED_STATIC_INFORMATION_TYPES = {
    "string",
    "number",
    "float",
    "boolean",
    "json",
    "date",
    "time",
    "datetime",
}


class KeyValueInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyValueInformation
        fields = ["id", "name", "title", "value", "as_type"]
        read_only_fields = ["id"]

    def validate_as_type(self, value: str) -> str:
        normalized = (value or "").strip().lower()
        if normalized not in ALLOWED_STATIC_INFORMATION_TYPES:
            raise serializers.ValidationError("Недопустимый тип данных.")
        return normalized


class KeyValueInformationPublicSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="as_type", read_only=True)

    class Meta:
        model = KeyValueInformation
        fields = ["name", "value", "type"]
        read_only_fields = fields


class ContactsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactsGroups
        fields = ["id", "name"]
        read_only_fields = ["id"]


class ContactSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )

    class Meta:
        model = Contacts
        fields = [
            "id",
            "main_title",
            "subtitle",
            "phone_numbers",
            "group",
            "priority",
        ]
        read_only_fields = ["id"]

    def validate_phone_numbers(self, value: list[Any]) -> list[str]:
        if not value:
            raise serializers.ValidationError("Необходимо указать хотя бы один номер.")

        try:
            validate_phone_numbers(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        return [str(item) for item in value]


class ContactPublicSerializer(serializers.ModelSerializer):
    group = ContactsGroupSerializer(read_only=True)

    class Meta:
        model = Contacts
        fields = [
            "id",
            "main_title",
            "subtitle",
            "phone_numbers",
            "group",
        ]
        read_only_fields = fields
