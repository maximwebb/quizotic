from django.urls import path
from .views import lobby, teams, views, index
from .events import sse

urlpatterns = [
	path("", index.home_view, name="index"),
	path("lobby", lobby.lobby_view, name="lobby"),
	path("teams/create", teams.create, name="create_team"),
	path("teams/list", teams.list, name="team_list"),
	path("events/", sse),
]
