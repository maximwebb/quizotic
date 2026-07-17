from . import question
from django.shortcuts import render
from django.http import HttpResponse

import json
import os


def quiz_view(request):
	context = {}
	return question.mcq_view(request)

