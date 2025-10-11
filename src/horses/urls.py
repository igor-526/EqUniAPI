from django.urls import path

from .views import (
    BreedDetailAPIView,
    BreedListCreateAPIView,
    HorseDetailAPIView,
    HorseListCreateAPIView,
    HorseOwnersDetailAPIView,
    HorseOwnersListCreateAPIView,
    HorsePedigreeAPIView,
)

urlpatterns = [
    path("", HorseListCreateAPIView.as_view()),
    path("<int:pk>/", HorseDetailAPIView.as_view()),
    path("<int:pk>/pedigree/<str:mode>/", HorsePedigreeAPIView.as_view()),
    path("breeds/", BreedListCreateAPIView.as_view()),
    path("breeds/<int:pk>/", BreedDetailAPIView.as_view()),
    path("owners/", HorseOwnersListCreateAPIView.as_view()),
    path("owners/<int:pk>/", HorseOwnersDetailAPIView.as_view()),
]
