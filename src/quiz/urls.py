from django.urls import path
from .views import lobby, teams, views, index, game, controller
from .events import sse

urlpatterns = [
	path("", index.home_view, name="index"),
	path("lobby", lobby.lobby_view, name="lobby"),
	path("teams/create", teams.create, name="create_team"),
	path("teams/list", teams.list, name="team_list"),
	path("game", game.game_view, name="game"),
	path("controller", controller.controller_view, name="controller"),
	path("events/", sse),
]
