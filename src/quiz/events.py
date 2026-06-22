import time
from django.http import StreamingHttpResponse

def event_stream():
	i = 0
	while True:
		payload = f'event: update\ndata: {{"foo": {i}}}\n\n'
		i += 1
		print(f"Sending: {payload}")
		yield payload
		time.sleep(5)

def sse(request):
	return StreamingHttpResponse(
		event_stream(),
		content_type="text/event-stream"
	)
