from django.conf import settings
from django.utils import timezone

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class JWTRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_cookie_name = settings.SIMPLE_JWT["AUTH_COOKIE"]
        refresh_cookie_name = settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"]

        request._jwt_new_access_token = None
        request._jwt_new_refresh_token = None
        request._jwt_clear_tokens = False

        access_token = request.COOKIES.get(access_cookie_name)

        if access_token:
            try:
                AccessToken(access_token)
                self._set_authorization_header(request, access_token)
            except TokenError:
                self._try_refresh(request, refresh_cookie_name)
        else:
            self._try_refresh(request, refresh_cookie_name)

        response = self.get_response(request)

        if request._jwt_new_access_token:
            access_expires = (
                timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
            )
            response.set_cookie(
                key=access_cookie_name,
                value=request._jwt_new_access_token,
                expires=access_expires,
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            )

        if request._jwt_new_refresh_token:
            refresh_expires = (
                timezone.now() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
            )
            response.set_cookie(
                key=refresh_cookie_name,
                value=request._jwt_new_refresh_token,
                expires=refresh_expires,
                httponly=True,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                path=settings.SIMPLE_JWT["REFRESH_COOKIE_PATH"],
            )

        if request._jwt_clear_tokens:
            response.delete_cookie(
                key=access_cookie_name,
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            )
            response.delete_cookie(
                key=refresh_cookie_name,
                path=settings.SIMPLE_JWT["REFRESH_COOKIE_PATH"],
            )

        return response

    def _try_refresh(self, request, refresh_cookie_name):
        refresh_token = request.COOKIES.get(refresh_cookie_name)

        if not refresh_token:
            return

        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            request._jwt_clear_tokens = True
            return

        new_access_token = str(refresh.access_token)
        self._set_authorization_header(request, new_access_token)
        request._jwt_new_access_token = new_access_token

        if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS"):
            request._jwt_new_refresh_token = str(refresh)

    @staticmethod
    def _set_authorization_header(request, token):
        if "HTTP_AUTHORIZATION" not in request.META:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
