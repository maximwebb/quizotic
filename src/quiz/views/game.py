from django.shortcuts import render
from django.http import HttpResponse

def game_view(request):
	context = {}
	return render(request, "game/index.html", context)
