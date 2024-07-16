# app/urls.py

from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/new/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
]
