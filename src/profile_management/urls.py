from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from profile_management.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    UserInfoRetrieveAPIView,
)

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view()),
    path("token/refresh/", CustomTokenRefreshView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("user/<int:pk>/", UserInfoRetrieveAPIView.as_view()),
    path("user/", UserInfoRetrieveAPIView.as_view()),
]
