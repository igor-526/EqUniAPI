from django.urls import path

from .views import (
    ContactDetailAPIView,
    ContactGroupDetailAPIView,
    ContactGroupListCreateAPIView,
    ContactListCreateAPIView,
    KeyValueInformationDetailAPIView,
    KeyValueInformationListCreateAPIView,
)

urlpatterns = [
    path("", KeyValueInformationListCreateAPIView.as_view(), name="static-info-list"),
    path(
        "<int:pk>/",
        KeyValueInformationDetailAPIView.as_view(),
        name="static-info-detail",
    ),
    path(
        "contacts/groups/",
        ContactGroupListCreateAPIView.as_view(),
        name="contacts-groups-list",
    ),
    path(
        "contacts/groups/<int:pk>/",
        ContactGroupDetailAPIView.as_view(),
        name="contacts-groups-detail",
    ),
    path("contacts/", ContactListCreateAPIView.as_view(), name="contacts-list"),
    path(
        "contacts/<int:pk>/",
        ContactDetailAPIView.as_view(),
        name="contacts-detail",
    ),
]
