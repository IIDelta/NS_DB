from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('add-keyword/', views.ProjectListView.add_keyword, name='add-keyword'),
    path('delete-keyword/', views.ProjectListView.delete_keyword, name='delete-keyword'),
    path('update-project-status/', views.update_project_status, name='update-project-status'),
    path('update-therapeutic-areas/', views.update_therapeutic_areas, name='update-therapeutic-areas'),
    path('update-deliverables/', views.update_deliverables, name='update-deliverables'),
    path('update-ingredient-categories/', views.update_ingredient_categories, name='update-ingredient-categories'),
    path('update-responsible-parties/', views.update_responsible_parties, name='update-responsible-parties'),
    path('update-route-of-admin/', views.update_route_of_admin, name='update-route-of-admin'),
    path('update-ingredients/', views.update_ingredients, name='update_ingredients'),
    path('update-demographics/', views.update_demographics, name='update-demographics'),

]
