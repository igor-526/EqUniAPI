from typing import Any, ClassVar
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group

from profile_management.permissions import UserPermission
from profile_management.swager_schemas import CustomTokenObtainPairViewExtendSchema, LogoutViewExtendSchema, UserInfoRetrieveAPIViewExtendSchema, UserListCreateAPIViewExtendSchema, UserPageMetaDataAPIViewExtendSchema, UserRetrieveUpdateDestroyAPIViewExtendSchema

from .models import NewUser
from .serializers import UserPageMetadataSerializer, UserSelfSerializer, UserSerializer


@extend_schema(tags=["Пользователи: авторизация"])
@extend_schema_view(**CustomTokenObtainPairViewExtendSchema)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")
            access_token_expires = timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
            refresh_token_expires = timezone.now() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]

            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=access_token,
                expires=access_token_expires,
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"],
                value=refresh_token,
                expires=refresh_token_expires,
                httponly=True,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                path=settings.SIMPLE_JWT["REFRESH_COOKIE_PATH"],
            )

            response.data = {"status": "ok"}

        return response


@extend_schema(tags=["Пользователи: авторизация"])
@extend_schema_view(**LogoutViewExtendSchema)
class LogoutView(APIView):
    def post(self, request):
        response = Response({"status": "ok"})
        response.delete_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.delete_cookie(
            key=settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"],
            path=settings.SIMPLE_JWT["REFRESH_COOKIE_PATH"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        return response


@extend_schema(tags=["Пользователи: авторизация"])
@extend_schema_view(**UserInfoRetrieveAPIViewExtendSchema)
class UserInfoRetrieveAPIView(RetrieveAPIView):
    model = NewUser
    serializer_class = UserSelfSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewUser.objects.all()

    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance, many=False, context={"request": request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=["Пользователи: администрирование"])
@extend_schema_view(**UserListCreateAPIViewExtendSchema)
class UserListCreateAPIView(APIView):
    model = NewUser
    permission_classes = [UserPermission]
    serializer_class = UserSerializer

    def build_query_dict(self, *args, **kwargs) -> dict[str, Any]:
        query_params = self.request.query_params

        search_username = query_params.get("username", None)
        search_email = query_params.get("email", None)
        filter_groups = query_params.getlist("groups[]", None)

        query_dict = dict()

        if search_username is not None:
            query_dict["username__icontains"] = search_username

        if search_email is not None:
            query_dict["email__icontains"] = search_email

        if filter_groups:
            query_dict["groups__id__in"] = filter_groups

        return query_dict

    def get_sort_list(self, *args, **kwargs):
        query_params = self.request.query_params

        sort_params = query_params.getlist("sort[]")
        sort_list = list()
        if sort_params:
            for param in sort_params:
                if param == "name":
                    sort_list.append("last_name")
                elif param == "-name":
                    sort_list.append("-last_name")
                elif param in [
                    "username",
                    "-username",
                    "email",
                    "-email",
                ]:
                    sort_list.append(param)
        return sort_list

    def get_queryset(self, *args, **kwargs):
        queryset = (
            NewUser.objects.prefetch_related("groups")
        )

        search_full_name = self.request.query_params.get("name", None)

        if search_full_name:
            splitted_fullname = search_full_name.split(" ")
            q = Q()
            for query in splitted_fullname:
                q |= Q(first_name__icontains=query)
                q |= Q(last_name__icontains=query)
                q |= Q(patronymic__icontains=query)
            queryset = queryset.filter(q)

        return queryset.filter(**self.build_query_dict()).order_by(
            *self.get_sort_list()
        ).distinct()

    def paginate_queryset(self, queryset):
        query_params = self.request.query_params
        qp_limit = query_params.get("limit")
        qp_offset = query_params.get("offset")

        try:
            qp_limit = int(qp_limit)
            if qp_limit < 1:
                qp_limit = 1
            elif qp_limit > 100:
                qp_limit = 100
        except (ValueError, TypeError):
            qp_limit = 50

        try:
            qp_offset = int(qp_offset)
            if qp_offset < 0:
                qp_offset = 0
        except (ValueError, TypeError):
            qp_offset = 0

        return queryset[qp_offset : qp_limit + qp_offset]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        queryset = self.paginate_queryset(queryset)

        serializer_data = self.serializer_class(
            queryset,
            many=True,
            context={"request": request},
        ).data
        return Response(
            data={"count": count, "items": serializer_data}, status=status.HTTP_200_OK
        )
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if "groups[]" in data and "groups" not in data:
            data["groups"] = data.pop("groups[]")

        serializer = self.serializer_class(
            data=data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = self.serializer_class(
            instance=user,
            context={"request": request},
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Пользователи: администрирование"])
@extend_schema_view(**UserRetrieveUpdateDestroyAPIViewExtendSchema)
class UserRetrieveUpdateDestroyAPIView(APIView):
    model = NewUser
    permission_classes = [UserPermission]
    serializer_class = UserSerializer

    def patch(self, request, user_id: int, *args, **kwargs):
        try:
            user = NewUser.objects.get(id=user_id)
        except NewUser.DoesNotExist:
            return Response(data={"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        if "groups[]" in data and "groups" not in data:
            data["groups"] = data.pop("groups[]")

        serializer = self.serializer_class(
            data=data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.update(user, serializer.data)
        response_serializer = self.serializer_class(
            instance=user,
            context={"request": request},
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id: int, *args, **kwargs):
        try:
            user = NewUser.objects.get(id=user_id)
        except NewUser.DoesNotExist:
            return Response(data={"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        if user.id == self.request.user.id:
            return Response(data={"detail": "Вы не можете удалить самого себя"}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@extend_schema(tags=["Пользователи: администрирование"])
@extend_schema_view(**UserPageMetaDataAPIViewExtendSchema)
class UserPageMetaDataAPIView(APIView):
    permission_classes = [UserPermission]
    serializer_class = UserPageMetadataSerializer

    def get(self, request, *args, **kwargs):
        data = {
            "user_groups": Group.objects.all()
        }
        serializer = self.serializer_class(data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)