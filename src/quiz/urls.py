from django.urls import path
from .views import lobby, teams, views

urlpatterns = [
	path("", views.index, name="index"),
	path("lobby", lobby.lobby_view, name="lobby"),
	path("teams/create", teams.create, name="create_team")
]
