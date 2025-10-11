from django.urls import path

from .views import (
    PhotoCategoryListCreateAPIView,
    PhotoCategoryRetrieveUpdateDestroyAPIView,
    PhotoListCreateAPIView,
    PhotoRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", PhotoListCreateAPIView.as_view()),
    path("<int:pk>/", PhotoRetrieveUpdateDestroyAPIView.as_view()),
    path("category/", PhotoCategoryListCreateAPIView.as_view()),
    path("category/<int:pk>/", PhotoCategoryRetrieveUpdateDestroyAPIView.as_view()),
]
