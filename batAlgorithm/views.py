from django.shortcuts import render
import numpy as np
import random
import math
import json
from django.http import JsonResponse
from django.http import HttpResponse
import random
import random 
import json
from NatureInspiredHybridAlgoToolbox import benchmark_functions

details = "particles","variables", "min_v", "max_v", "function" 
data = {}

def index(request):
	return render(request,'bat.html')

def search(request):
	for i in details:
		data[i] = request.GET.get(i)
	return HttpResponse(json.dumps(data))

def run(request):
	for i in range(1):
		Algorithm = BatAlgorithm(int(request.GET.get('d')), int(request.GET.get('np')), int(request.GET.get('n_gen')), int(request.GET.get('a')), int(request.GET.get('r')), int(request.GET.get('qmin')), int(request.GET.get('qmax')), int(request.GET.get('lower')), int(request.GET.get('upper')), request.GET.get('function'))
		result = Algorithm.move_bat()
	patternTitle = r'<\s*h3\s*><[^>]*>[^(<)]*'
	#print (result)

	return HttpResponse(result, content_type="application/json")




class BatAlgorithm():
    def __init__(self, D, NP, N_Gen, A, r, Qmin, Qmax, Lower, Upper, function):
        self.D = D  #dimension
        self.NP = NP  #population size 
        self.N_Gen = N_Gen  #generations
        self.A = A  #loudness
        self.r = r  #pulse rate
        self.Qmin = Qmin  #frequency min
        self.Qmax = Qmax  #frequency max
        self.Lower = Lower  #lower bound
        self.Upper = Upper  #upper bound

        self.f_min = 0.0  #minimum fitness
        
        self.Lb = [0] * self.D  #lower bound
        self.Ub = [0] * self.D  #upper bound
        self.Q = [0] * self.NP  #frequency

        self.v = [[0 for i in range(self.D)] for j in range(self.NP)]  #velocity
        self.Sol = [[0 for i in range(self.D)] for j in range(self.NP)]  #population of solutions
        self.Fitness = [0] * self.NP  #fitness
        self.best = [0] * self.D  #best solution
        self.Fun_val = function
        self.output = {}
        self.object_function_count = int(0)

    def Fun(self,D,sol):
        val = 0.0
        # print(D,sol)
        # for i in range(D):
        #     val = val + sol[i] * sol[i]
        params = {'d':D,'sol':sol}
        value = float(0)
        item = {}
        value = benchmark_functions.function(int(self.Fun_val),params)
        item["bestSolutionForIteration"] = value
        self.output[self.object_function_count] = item
        self.object_function_count +=1
        #print(value)
        return value

    def best_bat(self):
        i = 0
        j = 0
        for i in range(self.NP):
            if self.Fitness[i] < self.Fitness[j]:
                j = i
        for i in range(self.D):
            self.best[i] = self.Sol[j][i]
        self.f_min = self.Fitness[j]

    def init_bat(self):
        for i in range(self.D):
            self.Lb[i] = self.Lower
            self.Ub[i] = self.Upper

        for i in range(self.NP):
            self.Q[i] = 0
            for j in range(self.D):
                rnd = random.uniform(0, 1)
                self.v[i][j] = 0.0
                self.Sol[i][j] = self.Lb[j] + (self.Ub[j] - self.Lb[j]) * rnd
            self.Fitness[i] = self.Fun(self.D, self.Sol[i])
        self.best_bat()

    def simplebounds(self, val, lower, upper):
        if val < lower:
            val = lower
        if val > upper:
            val = upper
        return val

    def move_bat(self):
        S = [[0.0 for i in range(self.D)] for j in range(self.NP)]

        self.init_bat()
 		
        value =[]
        iteration = []
        for t in range(self.N_Gen):
            
            generation = []
            value.append(self.f_min)
			
            for i in range(self.NP):
                rnd = random.uniform(0, 1)
                self.Q[i] = self.Qmin + (self.Qmin - self.Qmax) * rnd
                for j in range(self.D):
                    self.v[i][j] = self.v[i][j] + (self.Sol[i][j] -
                                                   self.best[j]) * self.Q[i]
                    S[i][j] = self.Sol[i][j] + self.v[i][j]

                    S[i][j] = self.simplebounds(S[i][j], self.Lb[j],
                                                self.Ub[j])

                rnd = random.random

                if rnd > self.r:
                    for j in range(self.D):
                        S[i][j] = self.best[j] + 0.001 * random.gauss(0, 1)

                Fnew = self.Fun(self.D, S[i])

                generation.append(Fnew)

                rnd = random.random

                if (Fnew <= self.Fitness[i]) and (rnd < self.A):
                    for j in range(self.D):
                        self.Sol[i][j] = S[i][j]
                    self.Fitness[i] = Fnew

                if Fnew <= self.f_min:
                    for j in range(self.D):
                        self.best[j] = S[i][j]
                    self.f_min = Fnew

            # iteration.append(dict([(ii,generation[ii]) for ii in range(len(generation))]))
            iteration.append(generation)

        #print (self.f_min)
        size = len(iteration)
      	
      	#gwen = dict([(ii,nu[ii]) for ii in range(size)])
      	#print gwen
        #data = dict([(ii,bomb[ii]) for ii in range(size)])
        # result = {}
        # result["total iterations"]=iteration
        # result["best_solution"]=self.f_min
        # result["iteration"] = t
        self.output["length"] = self.object_function_count
        return JsonResponse(self.output)
