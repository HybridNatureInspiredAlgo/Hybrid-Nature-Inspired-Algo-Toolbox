from django.shortcuts import render
import numpy as np
import random
import math
import json
from django.http import JsonResponse
from django.http import HttpResponse



# Start location
x_start = [-2, -4]


def f(x,y):
    x1 = x[0]
    x2 = x[1]
    if y == 1:
    	obj = x1**2 + x2**3 + 1
    elif y == 2:
    	obj = x1**3 + x2 + 1
    else:
    	obj = x1**2 + x2**2
    # obj = 5 + x1**2 + x2**2 - 0.1*math.cos(6.0*3.1415*x1) - 0.1*math.cos(6.0*3.1415*x2)
    return obj



def index(request):
	# Number of cycles
	n = 1000

	# Number of trials per cycle
	m = 1000
	na = 0.0
	p1 = 0.7
	p50 = 0.001
	t1 = -1.0/math.log(p1)
	t50 = -1.0/math.log(p50)

	# Fractional reduction every cycle
	frac = (t50/t1)**(1.0/(n-1.0))
	
	# Initialize x
	x = np.zeros((n+1,2))
	x[0] = x_start
	xi = np.zeros(2)
	xi = x_start
	na = na + 1.0

	# Current best results so far
	y = int(request.GET.get('function'))
	xc = np.zeros(2)
	xc = x[0]
	fc = f(xi,y)
	fs = np.zeros(n+1)
	fs[0] = fc

	# Current temperature
	t = t1
	DeltaE_avg = 0.0

	temperature_itt = {}
	temperature_itt['temperature'] = {}
	

	for i in range(n):
	    for j in range(m):
	        # Generate new trial points
	        xi[0] = xc[0] + random.random() - 0.8
	        xi[1] = xc[1] + random.random() - 0.8

	        # Clip to upper and lower bounds
	        xi[0] = max(min(xi[0],int(request.GET.get('max_v'))),int(request.GET.get('min_v')))
	        xi[1] = max(min(xi[1],int(request.GET.get('max_v'))),int(request.GET.get('min_v')))

	        DeltaE = abs(f(xi,y)-fc)
	        if (f(xi,y)<fc):
	            if (i==0 and j==0): DeltaE_avg = DeltaE
	            p = math.exp(-DeltaE/(DeltaE_avg * t))
	            if (random.random()>p):
	                accept = True
	            else:
	                accept = False
	        else:
	            accept = True
	        if (accept==True):
	            xc[0] = xi[0]
	            xc[1] = xi[1]
	            fc = f(xc,y)
	            na = na + 1.0
	            DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na
	    x[i+1][0] = xc[0]
	    x[i+1][1] = xc[1]
	    fs[i+1] = fc
	    t = frac * t

	    temperature_itt['temperature'][i] =   str(t)
	    print ('Iteration: %d temperature: %10.5f' %(i,t))

	temperature_itt['best_solution'] = str(xc)
	temperature_itt['best_objective'] = str(fc)

	return JsonResponse(temperature_itt)

