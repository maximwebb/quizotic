from .views import controller, index, teams, question, quiz

from django.urls import path, include
import django_eventstream
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path("", index.home_view, name="index"),
    path("teams/create", teams.create, name="create_team"),
    path("teams/list", teams.list, name="team_list"),
    path("quiz", quiz.quiz_view, name="quiz"),
    path("controller/<int:game_id>", controller.game_view, name="controller_game"),
    path("controller/<int:game_id>/state", controller.game_state_view, name="controller_game_state"),
    path("controller", controller.game_select_view, name="controller_select"),
    path("game/<int:game_id>/<str:action>", controller.game_action, name="game_action"),
    path("game/<int:game_id>/room/<str:room>", controller.game_room, name="game_room"),
    path("game/<int:game_id>", controller.game, name="game"),
    path("game", controller.game, name="game_list"),
    path("create-quiz", controller.create_quiz_from_file, name="create_quiz"),
    path("events/", include(django_eventstream.urls), {"channels": ["events"]}),
]
