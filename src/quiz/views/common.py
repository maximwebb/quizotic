from ..models import GameState, Team


def get_game_by_code(code):
    return GameState.objects.filter(code=code)[0]


def get_cur_team(request):
    name = request.session["team_name"]
    return Team.objects.filter(team_name=name)[0]
