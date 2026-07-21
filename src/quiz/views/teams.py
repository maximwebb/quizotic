from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.urls import reverse

from .common import get_game_by_code
from .lobby import lobby_view
from ..forms import CreateTeamForm
from ..models import Team, GameState
from .. import events


def create(request, game_code: int):
    if request.method == "POST":
        context = {}
        team_name = request.POST["team_name"]
        team_leader = request.POST["team_leader"]
        request.session["team_name"] = team_name

        print(game_code)
        game = get_game_by_code(game_code)
        team = Team(team_name=team_name, team_leader=team_leader, game=game)
        team.save()

        events.push_teams_update()

        return HttpResponseRedirect(reverse(f"quiz", args=(game_code,)))

    elif request.method == "GET":
        form = CreateTeamForm()
        context = {"form": form}

        return render(request, "teams/create.html", context)

    return HttpResponseNotFound()


# TODO: Scope to game code
def list(request):
    teams = Team.objects.all()
    return render(request, "teams/list.html", {"teams": teams})
