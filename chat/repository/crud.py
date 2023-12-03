from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import exceptions as rest_execeptions, status
from chat.models import ChatRooms, Message
from . import constants
from .schemas import MessageSchema


def enter_chat_room(user: User, room_name: str) -> ChatRooms:
    chat_room = ChatRooms.objects.get(room_name=room_name)
    if len(chat_room.members.all()) == settings.MAX_MEMBERS_IN_ROOMS:
        raise rest_execeptions.APIException(
            code=status.HTTP_400_BAD_REQUEST, detail="Group full"
        )
    return chat_room.enter_room(user=user)


def leave_chat_room(user: User, room_name: str) -> ChatRooms:
    chat_room = ChatRooms.objects.get(room_name=room_name)

    return chat_room.leave_room(user=user)


def create_chatroom_message(message_schema: MessageSchema):
    sender = User.objects.get(username=message_schema.sender)
    room = ChatRooms.objects.get(room_name=message_schema.room)
    if sender not in room.members:
        return None
    message = Message(**message_schema, sender=sender, room=room)
    message.save()
    return message


def find_change_room_by_name(name: str) -> bool:
    return ChatRooms.objects.filter(room_name=name).exists()
