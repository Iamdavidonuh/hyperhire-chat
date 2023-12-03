from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import exceptions as rest_execeptions, status
from chat.models import ChatRooms


def add_users_to_chatroom(user: User, room_name: str) -> ChatRooms:
    chat_room = ChatRooms.objects.get(room_name=room_name)
    if len(chat_room.members.all()) == settings.MAX_MEMBERS_IN_ROOMS:
        raise rest_execeptions.APIException(
            code=status.HTTP_400_BAD_REQUEST, detail="Group full"
        )

    if user not in chat_room.members:
        chat_room.members.add(user)
    return chat_room


def leave_chat_room(user: User, room_name: str) -> ChatRooms:
    chat_room = ChatRooms.objects.get(room_name=room_name)

    if user in chat_room.members:
        chat_room.members.remove(user)
    return chat_room
