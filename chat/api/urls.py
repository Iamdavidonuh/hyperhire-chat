from django.urls import include, path
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()


router.register("chat-rooms", viewsets.ListCreateChatRoom, "chat_rooms")
router.register("chat-rooms/enter", viewsets.EnterChatRoom, "enter_chat_room")
router.register("chat-rooms/leave", viewsets.LeaveChatRoom, "leave_chat_room")
router.register("chat-rooms/message", viewsets.SendMessage, "send_message")


urlpatterns = [
    path("", include(router.urls)),
]
