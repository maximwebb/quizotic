from ..models import GameState, Team


def get_cur_game_state(request):
    return GameState.objects.all().order_by("-created")[0]


def get_cur_team(request):
    name = request.session["team_name"]
    return Team.objects.filter(team_name=name)[0]
