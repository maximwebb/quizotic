import time
from django.http import StreamingHttpResponse
from collections import deque

EVENT_QUEUE = deque()

def event_stream():
	i = 0
	while True:
		if EVENT_QUEUE:
			yield EVENT_QUEUE.pop()
		time.sleep(5)

def sse(request):
	return StreamingHttpResponse(
		event_stream(),
		content_type="text/event-stream"
	)
