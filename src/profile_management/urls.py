from django.urls import path

from profile_management.views import (
    UserListCreateAPIView,
    UserPageMetaDataAPIView,
    UserRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path("", UserListCreateAPIView.as_view()),
    path("<int:user_id>", UserRetrieveUpdateDestroyAPIView.as_view()),
    path("page_metadata", UserPageMetaDataAPIView.as_view())
]
