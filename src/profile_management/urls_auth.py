from django.urls import path

from profile_management.views import (
    CustomTokenObtainPairView,
    LogoutView,
    UserInfoRetrieveAPIView,
)

urlpatterns = [
    path("token", CustomTokenObtainPairView.as_view()),
    path("logout", LogoutView.as_view()),
    path("me", UserInfoRetrieveAPIView.as_view()),
]
