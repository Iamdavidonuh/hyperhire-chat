import json

from channels import exceptions as channels_exceptions
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core import exceptions

from chat.repository import crud
from chat.repository.schemas import MessageSchema


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user: User = await database_sync_to_async(self.get_user)(
            user=self.scope["user"]
        )
        room_name = self.scope["url_route"]["kwargs"]["room_name"]

        if not database_sync_to_async(crud.find_change_room_by_name)(room_name):
            raise channels_exceptions.DenyConnection("Room not Found")

        self.room_name = room_name
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_dict: dict = text_data_json["message"]
        message_schema = MessageSchema(
            **message_dict, sender=self.user.username, room=self.room_name
        )
        success = await database_sync_to_async(crud.create_chatroom_message)(
            message_schema=message_schema
        )
        if not success:
            raise exceptions.PermissionDenied(
                "You do not have permissions to send message to chatroom"
            )
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message_schema.to_dict()},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @staticmethod
    def get_user(user: User):
        try:
            return User.objects.get(pk=user.pk)
        except User.DoesNotExist:
            # would raise an error
            raise channels_exceptions.DenyConnection("User not Found")
