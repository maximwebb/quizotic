from django.shortcuts import render
from django.http import HttpResponse

def quiz_view(request):
	context = {}
	return render(request, "quiz/index.html", context)
