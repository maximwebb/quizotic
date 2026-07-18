from django.http import StreamingHttpResponse
from django_eventstream import send_event

from queue import Queue, Empty
import time


def push_teams_update():
    send_event("events", "update", {"type": "teams"})


def push_room_change():
    send_event("events", "refresh", {"type": "room_change"})


def push_question_change():
    send_event("events", "refresh", {"type": "question_change"})
