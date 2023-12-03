from django.urls import path, include

from . import views

urlpatterns = [
    path("", include("chat.api.urls")),
]
