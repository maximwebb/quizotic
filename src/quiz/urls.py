from .views import controller, index, teams, presenter, question, quiz, scoring

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
import django_eventstream
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path("", index.home_view, name="index"),
    path("teams/create/<str:game_code>", teams.create, name="create_team"),
    path("teams/list/<str:game_code>", teams.list, name="team_list"),
    path("teams/submitted/<str:game_code>", teams.submitted, name="team_submitted"),
    path("teams/profile/<str:game_code>", teams.profile, name="team_profile"),
    path("quiz/<str:game_code>", quiz.quiz_view, name="quiz"),
    path("controller/create", controller.create.create, name="create_game"),
    path("controller/<str:game_code>", controller.game.index, name="controller_game"),
    path("controller/<str:game_code>/state", controller.game.state, name="controller_game_state"),
    path("controller/<str:game_code>/position", controller.game.position, name="controller_game_position"),
    path("controller/<str:game_code>/marking", controller.marking.index, name="controller_marking"),
    re_path("controller/?", controller.create.index, name="controller_select"),
    path("game/<str:game_code>/<str:action>", controller.game.action, name="game_action"),
    path("scoreboard/<str:game_code>", scoring.scoreboard_view, name="scoreboard"),
    path("presenter/<str:game_code>", presenter.presenter_view, name="presenter"),
    path("canvas", index.canvas_view, name="canvas"),
    path("events/", include(django_eventstream.urls), {"channels": ["events"]}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
