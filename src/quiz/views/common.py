from ..models import GameState


def get_cur_game_state(request):
    return GameState.objects.all().order_by("-created")[0]
