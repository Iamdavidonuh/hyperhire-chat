from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


def signout(request):
    logout(request)
    return redirect(reverse("index"))
