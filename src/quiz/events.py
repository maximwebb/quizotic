import time
from django.http import StreamingHttpResponse
from collections import deque

EVENT_QUEUE = deque()

def event_stream():
	i = 0
	while True:
		push_teams_update()
		if EVENT_QUEUE:
			yield EVENT_QUEUE.pop()
		time.sleep(5)

def push_teams_update():
	payload = f'event: update\ndata: {{"type": "teams_update"}}\n\n'
	EVENT_QUEUE.appendleft(payload)


def push_room_update():
	payload = f'event: update\ndata: {{"type": "room_update"}}\n\n'
	EVENT_QUEUE.appendleft(payload)


def sse(request):
	return StreamingHttpResponse(
		event_stream(),
		content_type="text/event-stream"
	)
