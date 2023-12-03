from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import exceptions as rest_execeptions, status
from chat.models import ChatRooms, Message
from . import constants


def add_users_to_chatroom(user: User, room_name: str) -> ChatRooms:
    chat_room = ChatRooms.objects.get(room_name=room_name)
    if len(chat_room.members.all()) == settings.MAX_MEMBERS_IN_ROOMS:
        raise rest_execeptions.APIException(
            code=status.HTTP_400_BAD_REQUEST, detail="Group full"
        )
    return chat_room.enter_room(user=user)


def leave_chat_room(user: User, room_name: str) -> ChatRooms:
    chat_room = ChatRooms.objects.get(room_name=room_name)

    return chat_room.leave_room(user=user)


def create_text_message(sender: User, chat_room: ChatRooms, content: str):
    return Message.objects.create(
        message_type=constants.MessageType.TEXT, room=chat_room, text=content
    )
