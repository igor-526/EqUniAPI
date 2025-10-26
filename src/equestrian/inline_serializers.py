from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework.serializers import Serializer


def get_status_serializer(default: str | None = None) -> Serializer:
    return inline_serializer(
        name=f"StatusResponse{default if default else ''}", fields={"status": serializers.CharField(default=default)}
    )

def get_detail_serializer(default: str | None = None) -> Serializer:
    return inline_serializer(
        name=f"DetailResponse{default if default else ''}", fields={"detail": serializers.CharField(default=default)}
    )

def get_paginated_response_serializer(serializer: Serializer) -> Serializer:
    serializer_instance = serializer() if isinstance(serializer, type) else serializer
    serializer_name = serializer.__name__ if isinstance(serializer, type) else serializer.__class__.__name__

    items_field = serializers.ListSerializer(child=serializer_instance)

    inline_cls = inline_serializer(
        name=f"PaginatedResponse{serializer_name}",
        fields={"count": serializers.IntegerField(), "items": items_field},
    )

    return inline_cls
