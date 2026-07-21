from .views import controller, index, teams, question, quiz

from django.urls import path, include
import django_eventstream
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path("", index.home_view, name="index"),
    path("teams/create/<str:game_code>", teams.create, name="create_team"),
    path("teams/list/<str:game_code>", teams.list, name="team_list"),
    path("quiz/<str:game_code>", quiz.quiz_view, name="quiz"),
    path("controller/<str:game_code>", controller.game_view, name="controller_game"),
    path("controller/<str:game_code>/state", controller.game_state_view, name="controller_game_state"),
    path("controller", controller.game_select_view, name="controller_select"),
    path("game/<str:game_code>/<str:action>", controller.game_action, name="game_action"),
    path("game/<str:game_code>/room/<str:room>", controller.game_room, name="game_room"),
    path("game/<str:game_code>", controller.game, name="game"),
    path("game", controller.game, name="game_list"),
    path("create-quiz", controller.create_quiz_from_file, name="create_quiz"),
    path("canvas", index.canvas_view, name="canvas"),
    path("events/", include(django_eventstream.urls), {"channels": ["events"]}),
]
