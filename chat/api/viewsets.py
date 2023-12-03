from django.conf import settings
from rest_framework import exceptions as djr_exceptions
from rest_framework import generics, mixins, response, views, viewsets

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


class EnterChatRoom(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = chat_models.ChatRooms.objects.all()
    serializer_class = serializers.EnterChatRoomSerializer


class LeaveChatRoom(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = chat_models.ChatRooms.objects.all()
    serializer_class = serializers.LeaveChatRoomSerializer


class SendMessage(generics.CreateAPIView):
    queryset = chat_models.Message.objects.all()
    serializer_class = serializers.CreateMessageSerializer


class GetchatURL(views.APIView):
    def get_object(self, room_name):
        try:
            return chat_models.ChatRooms.objects.get(room_name=room_name)
        except chat_models.ChatRooms.DoesNotExist:
            raise djr_exceptions.NotFound

    def get(self, request, room_name, format=None):
        chat_room = self.get_object(room_name=room_name)

        url = f"ws://{settings.SITE_DOMAIN}/ws/chat/{chat_room.room_name}/"
        return response.Response(
            {"socket_connection_url": str(request.build_absolute_uri(url))}
        )
