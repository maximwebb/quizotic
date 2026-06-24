from django.shortcuts import render
from django.http import HttpResponse
from ..events import EVENT_QUEUE

def controller_view(request):
	if request.method == "PUT":
		print("Updating game state...")
		EVENT_QUEUE.appendleft('event: stateChange\ndata: {{}}\n\n')
		return HttpResponse("foo")

	context = {}
	return render(request, "controller.html", context)
