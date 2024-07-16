# app/urls.py

from django.urls import path
from .views import (
    ClientListView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
)

urlpatterns = [
    path("", ClientListView.as_view(), name="client-list"),
    path("project/", ProjectListView.as_view(), name="project-list"),
    path(
        "project/<str:pk>/", ProjectDetailView.as_view(), name="project-detail"
    ),  # Use <str:pk> for string primary keys
    path("project/new/", ProjectCreateView.as_view(), name="project-create"),
    path("project/<str:pk>/edit/", ProjectUpdateView.as_view(), name="project-edit"),
    path(
        "project/<str:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
]
