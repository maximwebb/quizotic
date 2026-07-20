from ..forms import JoinGameForm

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def home_view(request):
    form = JoinGameForm()
    context = {"form": form}
    return render(request, "index.html", context)


def canvas_view(request):
    return render(request, "include/canvas.html")
