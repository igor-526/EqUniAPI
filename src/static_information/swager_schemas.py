from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status

from .serializers import (
    ContactPublicSerializer,
    ContactSerializer,
    ContactsGroupSerializer,
    KeyValueInformationSerializer,
)

STATIC_INFO_PUBLIC_RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "value": {"type": "string"},
            "type": {"type": "string"},
        },
        "required": ["value", "type"],
    },
}

STATIC_INFO_TYPES_ENUM = [
    "string",
    "number",
    "float",
    "boolean",
    "json",
    "date",
    "time",
    "datetime",
]

KeyValueInformationListCreateAPIViewExtendSchema = {
    "get": extend_schema(
        tags=["Статичная информация"],
        summary="Получение статической информации",
        description=(
            "Возвращает словарь статической информации для публичного доступа. "
            "Если передан параметр `admin=true`, возвращается список записей "
            "со всеми полями (требуется роль EquestrianAdministrator)."
        ),
        parameters=[
            OpenApiParameter(
                name="admin",
                description="Включает административный формат ответа",
                required=False,
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="name[]",
                description="Список ключей информации (для публичного ответа)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                many=True,
            ),
            OpenApiParameter(
                name="name",
                description="Фильтр по ключу (для административного ответа)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="title",
                description="Фильтр по названию (для административного ответа)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="as_type[]",
                description="Фильтр по типу значения (для административного ответа)",
                required=False,
                location=OpenApiParameter.QUERY,
                enum=STATIC_INFO_TYPES_ENUM,
                type=OpenApiTypes.STR,
                many=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=STATIC_INFO_PUBLIC_RESPONSE_SCHEMA,
                description=(
                    "Публичный словарь или список записей в зависимости от параметра `admin`."
                ),
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Недостаточно прав для административного режима."
            ),
        },
    ),
    "post": extend_schema(
        tags=["Статичная информация"],
        summary="Создание записи статической информации",
        description="Создание новой записи (только для роли EquestrianAdministrator).",
        request=KeyValueInformationSerializer,
        responses={
            status.HTTP_201_CREATED: KeyValueInformationSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Ошибка валидации."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Недостаточно прав для выполнения операции."
            ),
        },
    ),
}

KeyValueInformationDetailAPIViewExtendSchema = {
    "get": extend_schema(
        tags=["Статичная информация"],
        summary="Получение записи статической информации",
        description="Возвращает запись по идентификатору (только для роли EquestrianAdministrator).",
        responses={
            status.HTTP_200_OK: KeyValueInformationSerializer,
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Недостаточно прав для выполнения операции."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Запись не найдена."),
        },
    ),
    "patch": extend_schema(
        tags=["Статичная информация"],
        summary="Обновление записи статической информации",
        description="Частичное обновление записи (только для роли EquestrianAdministrator).",
        request=KeyValueInformationSerializer,
        responses={
            status.HTTP_200_OK: KeyValueInformationSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Ошибка валидации."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Недостаточно прав для выполнения операции."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Запись не найдена."),
        },
    ),
    "delete": extend_schema(
        tags=["Статичная информация"],
        summary="Удаление записи статической информации",
        description="Удаляет запись (только для роли EquestrianAdministrator).",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Запись удалена."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Недостаточно прав для выполнения операции."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Запись не найдена."),
        },
    ),
}

ContactGroupListCreateAPIViewExtendSchema = {
    "get": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Список групп контактов",
        description="Возвращает список групп контактов. Требуется роль EquestrianAdministrator.",
        responses={
            status.HTTP_200_OK: ContactsGroupSerializer(many=True),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
        },
    ),
    "post": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Создание группы контактов",
        description="Создание новой группы контактов. Требуется роль EquestrianAdministrator.",
        request=ContactsGroupSerializer,
        responses={
            status.HTTP_201_CREATED: ContactsGroupSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Ошибка валидации."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
        },
    ),
}

ContactGroupDetailAPIViewExtendSchema = {
    "get": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Получение группы контактов",
        description="Возвращает группу контактов по идентификатору. Требуется роль EquestrianAdministrator.",
        responses={
            status.HTTP_200_OK: ContactsGroupSerializer,
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Группа не найдена."),
        },
    ),
    "patch": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Обновление группы контактов",
        description="Частичное обновление группы контактов. Требуется роль EquestrianAdministrator.",
        request=ContactsGroupSerializer,
        responses={
            status.HTTP_200_OK: ContactsGroupSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Ошибка валидации."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Группа не найдена."),
        },
    ),
    "delete": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Удаление группы контактов",
        description="Удаляет группу контактов. Требуется роль EquestrianAdministrator.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Группа удалена."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Группа не найдена."),
        },
    ),
}

ContactListCreateAPIViewExtendSchema = {
    "get": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Список контактов",
        description="Возвращает список контактов с фильтрацией. Доступно публично.",
        parameters=[
            OpenApiParameter(
                name="main_title",
                description="Фильтр по первичному наименованию (подстрока)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="subtitle",
                description="Фильтр по вторичному наименованию (подстрока)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="group[]",
                description="Список идентификаторов групп контактов",
                required=False,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                many=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: ContactPublicSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Ошибка валидации фильтра."),
        },
    ),
    "post": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Создание контакта",
        description="Создание контакта. Требуется роль EquestrianAdministrator.",
        request=ContactSerializer,
        responses={
            status.HTTP_201_CREATED: ContactSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Ошибка валидации."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
        },
    ),
}

ContactDetailAPIViewExtendSchema = {
    "get": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Получение контакта",
        description="Возвращает контакт по идентификатору. Требуется роль EquestrianAdministrator.",
        responses={
            status.HTTP_200_OK: ContactSerializer,
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Контакт не найден."),
        },
    ),
    "patch": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Обновление контакта",
        description="Частичное обновление контакта. Требуется роль EquestrianAdministrator.",
        request=ContactSerializer,
        responses={
            status.HTTP_200_OK: ContactSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Ошибка валидации."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Контакт не найден."),
        },
    ),
    "delete": extend_schema(
        tags=["Статичная информация: контакты"],
        summary="Удаление контакта",
        description="Удаляет контакт. Требуется роль EquestrianAdministrator.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Контакт удален."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Недостаточно прав."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Контакт не найден."),
        },
    ),
}
