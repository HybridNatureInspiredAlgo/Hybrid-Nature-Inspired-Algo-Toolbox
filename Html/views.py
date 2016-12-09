from django.shortcuts import render
import numpy as np
import random
import math
import json
from django.http import JsonResponse
from django.http import HttpResponse


details = "particles","variables", "min_v", "max_v", "function" 
data = {}

def index(request):
	return render(request,'form.html')

def search(request):
	for i in details:
		data[i] = request.GET.get(i)
	return HttpResponse(json.dumps(data))