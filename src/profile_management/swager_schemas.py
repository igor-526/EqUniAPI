from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import status

from equestrian.inline_serializers import (
    get_detail_serializer,
    get_paginated_response_serializer,
    get_status_serializer,
)
from profile_management.serializers import UserPageMetadataSerializer, UserSelfSerializer, UserSerializer

UserListCreateAPIViewExtendSchema = {
    "get": extend_schema(
        summary="Список пользователей",
        description="Получение списка всех пользователей",
        parameters=[
            OpenApiParameter(
                name="name",
                description="Поиск по ФИО (вхождение)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="username",
                description="Поиск по username (вхождение)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="email",
                description="Поиск по email (вхождение)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="groups[]",
                description="Поиск по группам (id)",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                many=True,
            ),
            OpenApiParameter(
                name="sort[]",
                description="Сортировка",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                enum=["name", "-name", "username", "-username", "email", "-email"],
                many=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=get_paginated_response_serializer(UserSerializer),
                description="Получение списка пользователей",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=get_detail_serializer("Учетные данные не были предоставлены."),
                description="Пользователь не авторизован",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=get_detail_serializer(
                    "У вас недостаточно прав для выполнения данного действия."
                ),
                description="Не добавлен в группу 'UserAdmin'",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="На сервере произошла ошибка"
            ),
        },
    ),
    "post": extend_schema(
        summary="Регистрация пользователя",
        description="Регистрация нового пользователя",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=UserSerializer,
                description="Пользователь успешно зарегистрирован",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Некорректные данные",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=get_detail_serializer("Учетные данные не были предоставлены."),
                description="Пользователь не авторизован",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=get_detail_serializer(
                    "У вас недостаточно прав для выполнения данного действия."
                ),
                description="Не добавлен в группу 'UserAdmin'",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="На сервере произошла ошибка"
            ),
        },
    ),
}

LogoutViewExtendSchema = {
    "post": extend_schema(
        summary="Логаут",
        description="Удаление токенов из httpOnly Cookies",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=get_status_serializer("ok"), description="Успешный логаут"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="На сервере произошла ошибка"
            ),
        },
    )
}

CustomTokenObtainPairViewExtendSchema = {
    "post": extend_schema(
        summary="Авторизация",
        description="Данные для JWT авторизации кладутся в httpOnly Cookies",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=get_status_serializer("ok"), description="Успешная авторизация"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=get_detail_serializer(
                    "Не найдено активной учетной записи с указанными данными"
                ),
                description="Неверный логин или пароль",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="На сервере произошла ошибка"
            ),
        },
    )
}

UserInfoRetrieveAPIViewExtendSchema = {
    "get": extend_schema(
        summary="Информация о пользователе",
        description="Возвращается информация об авторизованном пользователе",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSelfSerializer, description="Информация о пользователе"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=get_detail_serializer("Учетные данные не были предоставлены."),
                description="Пользователь не авторизован",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="На сервере произошла ошибка"
            ),
        },
    )
}

UserRetrieveUpdateDestroyAPIViewExtendSchema = {
    "patch": extend_schema(
        summary="Изменение пользователя",
        description="Изменение данных пользователя",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSerializer,
                description="Пользователь успешно изменён",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Некорректные данные",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=get_detail_serializer("Учетные данные не были предоставлены."),
                description="Пользователь не авторизован",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=get_detail_serializer(
                    "У вас недостаточно прав для выполнения данного действия."
                ),
                description="Не добавлен в группу 'UserAdmin'",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=get_detail_serializer("Пользователь не найден."),
                description="Пользователь не найден",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="На сервере произошла ошибка"
            ),
        },
    ),
    "delete": extend_schema(
        summary="Удаление пользователя",
        description="Безвозвратное удаление пользователя с потерей связанных данных",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Пользователь успешно удалён",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=get_detail_serializer("Вы не можете удалить самого себя"),
                description="Попытка удалить самого себя",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=get_detail_serializer("Учетные данные не были предоставлены."),
                description="Пользователь не авторизован",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=get_detail_serializer(
                    "У вас недостаточно прав для выполнения данного действия."
                ),
                description="Не добавлен в группу 'UserAdmin'",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=get_detail_serializer("Пользователь не найден."),
                description="Пользователь не найден",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="На сервере произошла ошибка"
            ),
        },
    ),
}


UserPageMetaDataAPIViewExtendSchema = {
    "get": extend_schema(
        summary="Метадата для страницы",
        description="Доступные группы пользователей",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserPageMetadataSerializer, description="Метадата"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=get_detail_serializer("Учетные данные не были предоставлены."),
                description="Пользователь не авторизован",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=get_detail_serializer(
                    "У вас недостаточно прав для выполнения данного действия."
                ),
                description="Не добавлен в группу 'UserAdmin'",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="На сервере произошла ошибка"
            ),
        },
    )
}