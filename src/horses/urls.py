from django.urls import path

from .views import (HorseDetailAPIView,
                    HorseListCreateAPIView,
                    HorsePedigreeAPIView)

urlpatterns = [
    path('', HorseListCreateAPIView.as_view()),
    path('<int:pk>/', HorseDetailAPIView.as_view()),
    path('<int:pk>/pedigree/<str:mode>/', HorsePedigreeAPIView.as_view())
]
