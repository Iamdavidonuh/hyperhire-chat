from rest_framework import serializers, exceptions
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from chat import models
from . import crud, schemas


channel_layer = get_channel_layer()


class ListCreateChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatRooms
        fields = "__all__"


class CreateChatRoomSerializer(serializers.ModelSerializer):
    current_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.ChatRooms
        fields = ["creator", "room_name"]

    def validate(self, attrs):
        if attrs["current_user"].pk != attrs["creator"].pk:
            raise exceptions.ValidationError(
                "The chat room's creator must be the logged in user"
            )
        return super().validate(attrs)


class EnterChatRoomSerializer(serializers.Serializer):
    hidden_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_pk = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        user = User.objects.filter(pk=attrs["user_pk"]).first()
        if not user:
            raise exceptions.ValidationError("No User Found")
        if user.pk != attrs["hidden_user"].pk:
            raise exceptions.ValidationError("User id not thesame with logged in user")
        return super().validate(attrs)

    def update(self, instance: models.ChatRooms, validated_data):
        user = User.objects.get(pk=validated_data["user_pk"])
        return instance.enter_room(user)


class LeaveChatRoomSerializer(serializers.Serializer):
    hidden_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_pk = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        user = User.objects.filter(pk=attrs["user_pk"]).first()
        if not user:
            raise exceptions.ValidationError("No User Found")
        if user.pk != attrs["hidden_user"].pk:
            raise exceptions.ValidationError("User id not thesame with logged in user")
        return super().validate(attrs)

    def update(self, instance: models.ChatRooms, validated_data):
        user = User.objects.get(pk=validated_data["user_pk"])
        return instance.leave_room(user)


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = "__all__"

    def validate(self, attrs):
        if attrs["user"] not in attrs["rooms"].members:
            raise exceptions.ValidationError(
                "Cannot send a message to a group you do not belong in"
            )
        return super().validate(attrs)

    def create(self, validated_data):
        instance: models.Message = super().create(validated_data)
        # send message via socket
        message = schemas.MessageSchema(
            text=instance.text,
            sender=instance.sender.username,
            media=instance.media.url,
            message_type=instance.message_type,
        )
        async_to_sync(channel_layer.group_send)(
            instance.room.room_name,
            {"type": "chat.message", "message": message.to_dict()},
        )
        return instance
