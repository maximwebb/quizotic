from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.urls import reverse

from .common import get_game_by_code, FileStore
from .lobby import lobby_view
from ..forms import CreateTeamForm, ProfilePicForm
from ..models import Team, GameState
from .. import events


def create(request, game_code: str):
    if request.method == "POST":
        context = {}
        team_name = request.POST["team_name"]
        team_leader = request.POST["team_leader"]
        request.session["team_name"] = team_name

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


def list(request, game_code: str):
    game = get_game_by_code(game_code)
    teams = Team.objects.filter(game=game)
    return render(request, "teams/list.html", {"teams": teams})


def profile(request, game_code: str):
    if request.method == "POST":
        files = request.FILES
        print(files)
        paths = []
        for k, v in files.items():
            path = FileStore.store(v, "")
            paths.append(path)
            with open(path) as f:
                data = f.read()
                print(data[:100])
        print(paths)
        return HttpResponseRedirect(reverse(f"quiz", args=(game_code,)))
    elif request.method == "GET":
        game = get_game_by_code(game_code)
        form = ProfilePicForm()
        context = {"game": game, "form": form}
        return render(request, "teams/profile.html", context)
