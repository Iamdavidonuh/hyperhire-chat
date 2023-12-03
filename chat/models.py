from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ChatRooms(models.Model):
    room_name = models.CharField(max_length=35, unique=True)
    members = models.ManyToManyField(User, related_name="conversations", blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"ChatRooms: {self.room_name}"

    def enter_room(self, user):
        if user not in self.members.all():
            self.members.add(user)
        return self

    def leave_room(self, user):
        if user in self.members.all():
            self.members.remove(user)
        return self


class Message(models.Model):
    class MessageType(models.TextChoices):
        TEXT = "TEXT", _("Text")
        MEDIA = "MEDIA", _("Media")

    message_type = models.CharField(
        max_length=5,
        choices=MessageType.choices,
        default=MessageType.TEXT,
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRooms, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    media = models.FileField(upload_to="contents", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def is_text(self):
        return self.message_type == Message.MessageType.TEXT

    @property
    def is_media(self):
        return self.message_type == Message.MessageType.MEDIA

    class Meta:
        ordering = ["-time_created"]

    def __str__(self) -> str:
        return f"Message From {self.sender}"
