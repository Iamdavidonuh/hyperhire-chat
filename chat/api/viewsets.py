from rest_framework import mixins, viewsets

from chat import models as chat_models
from chat.repository import serializers


class ListCreateChatRoom(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = chat_models.ChatRooms.objects.all()
    serializer_class = serializers.CreateChatRoomSerializer

    def get_serializer_class(self):
        if self.action in (
            "list",
            "retrieve",
        ):
            return serializers.ListCreateChatRoomSerializer
        return super().get_serializer_class()


class EnterChatRoom(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    queryset = chat_models.ChatRooms.objects.all()
    serializer_class = serializers.EnterChatRoomSerializer


class LeaveChatRoom(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    queryset = chat_models.ChatRooms.objects.all()
    serializer_class = serializers.LeaveChatRoomSerializer


class SendMessage(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = chat_models.Message.objects.all()
    serializer_class = serializers.CreateMessageSerializer
