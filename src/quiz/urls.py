from .views import lobby, teams, views, index, quiz, command
from .events import sse

from django.urls import path, include
from rest_framework import routers, serializers, viewsets

urlpatterns = [
	path("", index.home_view, name="index"),
	path("lobby", lobby.lobby_view, name="lobby"),
	path("teams/create", teams.create, name="create_team"),
	path("teams/list", teams.list, name="team_list"),
	path("quiz", quiz.quiz_view, name="quiz"),
	path("command", command.command_view, name="command"),
	path("game/<int:game_id>/<str:action>", command.game_action, name="game_action"),
	path("game/<int:game_id>", command.game, name="game"),
	path("game", command.game, name="game_list"),
	path("events/", sse),
]
