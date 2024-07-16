# app/urls.py

from django.urls import path
from .views import ClientListView  # Import the view

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client_list'),  # Map the URL to the view
]
