from django.urls import path

from profile_management.views import (
    CustomTokenObtainPairView,
    LogoutView,
    UserInfoRetrieveAPIView,
)

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("user/<int:pk>/", UserInfoRetrieveAPIView.as_view()),
    path("user/", UserInfoRetrieveAPIView.as_view()),
]
