from django.urls import path
from . import views

urlpatterns = [
    path("api/get-trending-data/", views.get_trending_data),
]
