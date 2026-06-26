from ..events import EVENT_QUEUE
from ..models import GameState

from django.shortcuts import render
from django.http import HttpResponse



def controller_view(request):
	context = {}
	games = GameState.objects.all().order_by("-created")
	print(f"Got game states: {games}")
	if games:
		game = games[0]
	else:
		return controller_create_game(request)

	context["game_id"] = game.pk
	return render(request, "controller.html", context)


def controller_api(request):
	print("Got API request")
	if request.method == "PUT":
		controller_create_game(request)
	
	if request.method == "PATCH":
		controller_update_game(request)


def controller_create_game(request):
	print("Creating new game!")
	game = GameState()
	game.save()
	context = {}
	context["game_id"] = game.pk
	return render(request, "controller.html", context)
	

def controller_update_game(request):
	print("Updating game state...")
	EVENT_QUEUE.appendleft('event: stateChange\ndata: {{}}\n\n')
	return HttpResponse("foo")
