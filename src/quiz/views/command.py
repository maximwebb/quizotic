from ..events import EVENT_QUEUE
from ..models import GameState 
from ..serializers import GameStateSerializer

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

import json


def command_view(request):
	context = {}
	games = GameState.objects.all().order_by("-created")

	context["games"] = games
	return render(request, "command/index.html", context)


def game(request, game_id=None):
	if game_id is None:
		if request.method == "POST":
			game = GameState()
			game.save()
			serializer = GameStateSerializer(game)
			return JsonResponse(serializer.data)
		elif request.method == "GET":
			games = GameState.objects.all().order_by("-created")
			serializer = GameStateSerializer(games, many=True)
			return JsonResponse(serializer.data, safe=False)
		else:
			return None
	
	if request.method == "GET":
		game = GameState.objects.values().get(pk=game_id)
		serializer = GameStateSerializer(game)
		return JsonResponse(serializer.data)

	return None
	

def game_action(request):
	pass
