from django.urls import path
from . import views

# URL patterns

app_name = "images"

urlpatterns = [
    path("create/", views.image_create, name="create"),
]
