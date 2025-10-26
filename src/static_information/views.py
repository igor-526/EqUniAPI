from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from .models import Contacts, ContactsGroups, KeyValueInformation
from .permissions import StaticInformationAdminPermission, is_equestrian_administrator
from .serializers import (
    ALLOWED_STATIC_INFORMATION_TYPES,
    ContactPublicSerializer,
    ContactSerializer,
    ContactsGroupSerializer,
    KeyValueInformationPublicSerializer,
    KeyValueInformationSerializer,
)
from .swager_schemas import (
    ContactDetailAPIViewExtendSchema,
    ContactGroupDetailAPIViewExtendSchema,
    ContactGroupListCreateAPIViewExtendSchema,
    ContactListCreateAPIViewExtendSchema,
    KeyValueInformationDetailAPIViewExtendSchema,
    KeyValueInformationListCreateAPIViewExtendSchema,
)


@extend_schema_view(**KeyValueInformationListCreateAPIViewExtendSchema)
class KeyValueInformationListCreateAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = KeyValueInformationSerializer

    @staticmethod
    def _is_admin_query(request) -> bool:
        return request.query_params.get("admin", "").lower() == "true"

    @staticmethod
    def _normalize_types(raw_types: list[str]) -> list[str]:
        normalized = [(item or "").strip().lower() for item in raw_types if item]
        invalid = [item for item in normalized if item not in ALLOWED_STATIC_INFORMATION_TYPES]
        if invalid:
            raise ValidationError({"as_type": "Недопустимое значение типа."})
        return normalized

    def _ensure_admin(self, request) -> None:
        if not is_equestrian_administrator(getattr(request, "user", None)):
            raise PermissionDenied("Недостаточно прав для выполнения действия.")

    def get_queryset(self):
        queryset = KeyValueInformation.objects.all()
        name = self.request.query_params.get("name")
        title = self.request.query_params.get("title")
        as_types = self.request.query_params.getlist("as_type[]")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if as_types:
            normalized = self._normalize_types(as_types)
            queryset = queryset.filter(as_type__in=normalized)

        return queryset.order_by("name")

    def get(self, request, *args, **kwargs):
        if self._is_admin_query(request):
            self._ensure_admin(request)
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = KeyValueInformation.objects.all().order_by("name")
        names = request.query_params.getlist("name[]")
        if names:
            queryset = queryset.filter(name__in=names)

        public_serializer = KeyValueInformationPublicSerializer(queryset, many=True)
        response_payload = {
            item["name"]: {"value": item["value"], "type": item["type"]}
            for item in public_serializer.data
        }
        return Response(response_payload, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self._ensure_admin(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(**KeyValueInformationDetailAPIViewExtendSchema)
class KeyValueInformationDetailAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = KeyValueInformationSerializer

    def _ensure_admin(self, request) -> None:
        if not is_equestrian_administrator(getattr(request, "user", None)):
            raise PermissionDenied("Недостаточно прав для выполнения действия.")

    def get_object(self, pk: int) -> KeyValueInformation:
        return get_object_or_404(KeyValueInformation, pk=pk)

    def get(self, request, pk: int, *args, **kwargs):
        self._ensure_admin(request)
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk: int, *args, **kwargs):
        self._ensure_admin(request)
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk: int, *args, **kwargs):
        self._ensure_admin(request)
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(**ContactGroupListCreateAPIViewExtendSchema)
class ContactGroupListCreateAPIView(APIView):
    permission_classes = [StaticInformationAdminPermission]
    serializer_class = ContactsGroupSerializer

    def get(self, request, *args, **kwargs):
        queryset = ContactsGroups.objects.all().order_by("name")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(**ContactGroupDetailAPIViewExtendSchema)
class ContactGroupDetailAPIView(APIView):
    permission_classes = [StaticInformationAdminPermission]
    serializer_class = ContactsGroupSerializer

    def get_object(self, pk: int) -> ContactsGroups:
        return get_object_or_404(ContactsGroups, pk=pk)

    def get(self, request, pk: int, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk: int, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk: int, *args, **kwargs):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(**ContactListCreateAPIViewExtendSchema)
class ContactListCreateAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ContactSerializer

    def _ensure_admin(self, request) -> None:
        if not is_equestrian_administrator(getattr(request, "user", None)):
            raise PermissionDenied("Недостаточно прав для выполнения действия.")

    def _parse_group_ids(self, raw_values: list[str]) -> list[int]:
        group_ids: list[int] = []
        for value in raw_values:
            try:
                group_ids.append(int(value))
            except (TypeError, ValueError) as exc:
                raise ValidationError({"group": "Идентификатор группы должен быть числом."}) from exc
        return group_ids

    def get_queryset(self) -> Any:
        queryset = Contacts.objects.select_related("group").all()
        query_params = self.request.query_params

        main_title = query_params.get("main_title")
        subtitle = query_params.get("subtitle")
        group_filters = query_params.getlist("group[]")

        if main_title:
            queryset = queryset.filter(main_title__icontains=main_title)

        if subtitle:
            queryset = queryset.filter(subtitle__icontains=subtitle)

        if group_filters:
            group_ids = self._parse_group_ids(group_filters)
            queryset = queryset.filter(group_id__in=group_ids)

        return queryset.order_by("group_id", "priority", "main_title", "subtitle")

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ContactPublicSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self._ensure_admin(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(**ContactDetailAPIViewExtendSchema)
class ContactDetailAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ContactSerializer

    def _ensure_admin(self, request) -> None:
        if not is_equestrian_administrator(getattr(request, "user", None)):
            raise PermissionDenied("Недостаточно прав для выполнения действия.")

    def get_object(self, pk: int) -> Contacts:
        return get_object_or_404(Contacts.objects.select_related("group"), pk=pk)

    def get(self, request, pk: int, *args, **kwargs):
        self._ensure_admin(request)
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk: int, *args, **kwargs):
        self._ensure_admin(request)
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk: int, *args, **kwargs):
        self._ensure_admin(request)
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
