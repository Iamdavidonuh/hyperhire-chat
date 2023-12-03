from django.urls import include, path

from . import views

urlpatterns = [
    path("", include("chat.api.urls")),
    path("logout/", views.signout, name="logout"),
    path("chat/", views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),
]
