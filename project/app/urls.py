from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('add-keyword/', views.ProjectListView.add_keyword, name='add-keyword'),
    path('delete-keyword/', views.ProjectListView.delete_keyword, name='delete-keyword'),
    path('update-project-status/', views.update_project_status, name='update-project-status'),
    path('update-therapeutic-areas/', views.update_therapeutic_areas, name='update-therapeutic-areas'),
    path('update-deliverables/', views.update_deliverables, name='update-deliverables'),

]
