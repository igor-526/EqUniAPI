from django.urls import path

from profile_management.views import UserInfoRetrieveAPIView

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/<int:pk>/', UserInfoRetrieveAPIView.as_view()),
    path('user/', UserInfoRetrieveAPIView.as_view()),
]
