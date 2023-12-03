from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from chat import models
from chat.repository import crud
from django.contrib.auth.models import User
import base64

# Create your tests here.


class TestChatEndpoints(APITestCase):
    def setUp(self) -> None:
        self.user = self.create_user()
        return super().setUp()

    @staticmethod
    def create_user(username=None, password=None):
        username = "testuser" or username
        password = "incorrect" or password
        return User.objects.create_user(username=username, password=password)

    def create_message(self, text=None):
        room = models.ChatRooms.objects.create(room_name="test", creator=self.user)
        return models.Message.objects.create(text=text, sender=self.user, room=room)

    def create_room(self, room_name=None):
        chat = models.ChatRooms.objects.create(room_name=room_name, creator=self.user)
        chat.enter_room(self.user)
        return chat

    def test_user_creates_chat_rooms(self):
        payload = {"room_name": "testing"}

        self.client.login(username=self.user.username, password="incorrect")
        credentials = base64.b64encode(b"testuser:incorrect").decode("utf-8")

        self.headers = {"Authorization": f"Basic {credentials}"}
        response = self.client.post(
            reverse("chat_rooms-list"), data=payload, headers=self.headers
        )
        self.assertTrue(
            models.ChatRooms.objects.filter(room_name="testing").exists(), True
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_sends_message(self):
        room = self.create_room(room_name="test_room")
        payload = {"text": "test message", "room": room.id, "message_type": "TEXT"}

        credentials = base64.b64encode(b"testuser:incorrect").decode("utf-8")

        self.headers = {"Authorization": f"Basic {credentials}"}
        response = self.client.post(
            reverse("send_message"), data=payload, headers=self.headers
        )
        self.assertTrue(
            models.Message.objects.filter(text=payload["text"]).exists(), True
        )
        assert response.status_code == status.HTTP_201_CREATED
