from django.urls import include, path
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()


router.register("chat-rooms", viewsets.ListCreateChatRoom, "chat_rooms")
router.register("chat-rooms/enter", viewsets.EnterChatRoom, "enter_chat_room")
router.register("chat-rooms/leave", viewsets.LeaveChatRoom, "leave_chat_room")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("django.contrib.auth.urls")),
    path("chat-rooms/message", viewsets.SendMessage.as_view(), name="send_message"),
    path(
        "chat-rooms/get-connection-url/<room_name>",
        viewsets.GetchatURL.as_view(),
        name="chat_room_conn_url",
    ),
]
