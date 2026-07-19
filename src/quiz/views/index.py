from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def home_view(request):
    return render(request, "index.html")


def canvas_view(request):
    return render(request, "include/canvas.html")
