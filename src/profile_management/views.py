from django.utils import timezone
from django.conf import settings
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import NewUser
from .serializers import UserSelfSerializer


@extend_schema(tags=["Пользователи"])
@extend_schema_view(
    get=extend_schema(
        summary="Информация о пользователе",
        description="Если id отсутствует, возвращается информация об авторизованном пользователе",
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED: None,
            status.HTTP_403_FORBIDDEN: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None, description="Описание 500 ответа"
            ),
        },
    )
)
class UserInfoRetrieveAPIView(RetrieveAPIView):
    model = NewUser
    serializer_class = UserSelfSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewUser.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get("pk")
            if user_id is None:
                instance = request.user
            else:
                instance = NewUser.objects.get(pk=kwargs["pk"])
        except NewUser.DoesNotExist:
            return Response(
                data={"detail": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(
            instance, many=False, context={"request": request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Пользователи"])
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


@extend_schema(tags=["Пользователи"])
class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Successfully logged out"})
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
