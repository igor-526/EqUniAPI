from datetime import datetime

from django.conf import settings

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .models import NewUser
from .serializers import UserSelfSerializer


class UserInfoRetrieveAPIView(RetrieveAPIView):
    model = NewUser
    serializer_class = UserSelfSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewUser.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get('pk')
            if user_id is None:
                instance = request.user
            else:
                instance = NewUser.objects.get(pk=kwargs['pk'])
        except NewUser.DoesNotExist:
            return Response(data={"detail": "Пользователь не найден"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(
            instance, many=False, context={'request': request})
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            refresh_token_expires = (
                    datetime.now() +
                    settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_COOKIE_NAME'],
                value=refresh_token,
                expires=refresh_token_expires,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax'
            )
            response.data = {'access': access_token}
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(
            settings.SIMPLE_JWT['REFRESH_COOKIE_NAME']
        )

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is missing'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            new_refresh_token = response.data.get('refresh')

            if new_refresh_token:
                refresh_token_expires = (
                        datetime.now() +
                        settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT['REFRESH_COOKIE_NAME'],
                    value=new_refresh_token,
                    expires=refresh_token_expires,
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite='Lax'
                )

            response.data = {'access': access_token}

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response({'detail': 'Successfully logged out'})
        response.delete_cookie(
            key=settings.SIMPLE_JWT['REFRESH_COOKIE_NAME'],
            samesite='Lax'
        )
        return response
