from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from rest_framework import exceptions, serializers

from chat import models

from . import schemas

channel_layer = get_channel_layer()


class ListCreateChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatRooms
        fields = "__all__"


class CreateChatRoomSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.ChatRooms
        fields = ["creator", "room_name"]

    def save(self, **kwargs):
        instance: models.ChatRooms = super().save(**kwargs)
        creator = User.objects.get(pk=instance.creator.pk)
        instance.members.add(creator)
        return instance


class EnterChatRoomSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance: models.ChatRooms, validated_data):
        user = User.objects.get(pk=validated_data["user"].pk)
        instance.enter_room(user)
        return instance


class LeaveChatRoomSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance: models.ChatRooms, validated_data):
        user = User.objects.get(pk=validated_data["user"].pk)
        instance.leave_room(user)
        return instance


class CreateMessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Message
        fields = "__all__"

    def validate(self, attrs):
        if attrs["sender"] not in attrs["room"].members.all():
            raise exceptions.ValidationError(
                "Cannot send a message to a group you do not belong in"
            )
        return super().validate(attrs)

    def create(self, validated_data):
        instance: models.Message = super().create(validated_data)
        # send message via socket
        message = schemas.MessageSchema(
            room=instance.room.pk,
            text=instance.text,
            sender=instance.sender.username,
            message_type=instance.message_type,
        )
        message.media = instance.media.url if instance.is_media else None
        channel_layer.group_send(
            instance.room.room_name,
            {"type": "chat.message", "message": message.to_dict()},
        )
        return instance


class ListMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = "__all__"
