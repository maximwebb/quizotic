from .. import events
from ..models import GameState 
from ..serializers import GameStateSerializer

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers

import json


# Game views

def game_select_view(request):
	context = {}
	games = GameState.objects.all().order_by("-created")

	context["games"] = games
	return render(request, "controller/index.html", context)


def game_view(request, game_id):
	if request.method == "GET":
		game = GameState.objects.values().get(pk=game_id)
		context = { "game": game }
		return render(request, "controller/game.html", context)


def game_state_view(request, game_id):
	if request.method == "GET":
		game = GameState.objects.get(pk=game_id)
		context = { "game": game }
		return render(request, "controller/game_state.html", context)


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
	

def game_action(request, game_id: int, action: str):
	game = GameState.objects.all().get(pk=game_id)
	if request.method == "POST":
		if action == "next-question":
			game.question += 1
		elif action == "prev-question":
			game.question -= 1
		else:
			return HttpResponseNotFound()

		game.save()
		serializer = GameStateSerializer(game)
		return JsonResponse(serializer.data)

	return HttpResponseNotFound()

def game_room(request, game_id: int, room: str=None):
	game = GameState.objects.all().get(pk=game_id)
	print(room)
	if request.method == "POST":
		if room == "lobby":
			game.room = GameState.Room.LOBBY
		elif room == "quiz":
			game.room = GameState.Room.QUIZ
		elif room == "round-end":
			game.room = GameState.Room.ROUND_END
		elif room == "game-end":
			game.room = GameState.Room.GAME_END
		else:
			return HttpResponseNotFound()
		game.save()
		serializer = GameStateSerializer(game)
		events.push_room_update()
		return JsonResponse(serializer.data)
		
	
	return HttpResponseNotFound()
