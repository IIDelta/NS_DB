# app/urls.py

from django.urls import path
from .views import (
    ClientListView,
    ProjectListView,
)

urlpatterns = [
    path("", ClientListView.as_view(), name="client-list"),
    path("project/", ProjectListView.as_view(), name="project-list"),
]
