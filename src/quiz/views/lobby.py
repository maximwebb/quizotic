from ..models import Team
from .common import get_game_by_code

from django.shortcuts import render
from django.http import HttpResponse


def lobby_view(request, game_code: str):
    team_dict = {}

    teams = Team.objects.all()
    team_name = request.session["team_name"]
    cur_team = Team.objects.get(team_name=team_name)

    context = {}
    context["game_code"] = game_code
    context["cur_team"] = cur_team
    context["game"] = get_game_by_code(game_code)

    return render(request, "lobby.html", context)
