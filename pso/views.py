from django.shortcuts import render
from django.http import HttpResponse
import random
import math
import copy
import sys
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run(request):
	functionCode = str(request.GET.get('functionCode','empty'))
	noOfParticles = request.GET.get('noOfParticles','empty')
	noOfIttration = request.GET.get('noOfIttration','empty')
	if functionCode == "5":
		variables = 10
	else:
		variables = 1
	
	num_particles = int(noOfParticles)
	max_ittrations = int(noOfIttration)
	min_v = request.GET.get('min_v','empty')
	max_v = request.GET.get('max_v','empty')

	print("particles = " + str(num_particles))
	print("max ittrations    = " + str(max_ittrations))
	finalData = Solve(max_ittrations, num_particles,variables, int(min_v) , int(max_v) , functionCode)
	best_position = finalData['best']
	printBestSolutionByPso(best_position)
	bestSol = getPresentMinValue(best_position , functionCode)
	#return HttpResponse("best solution = %.6f" % bestSol)
	return HttpResponse(finalData['report'])




def printBestSolutionByPso(vector):
	for i in range(len(vector)):
 		if i % 8 == 0:
 			print("\n" , end="")
 		if vector[i] >= 0.0:
 			print(' ', end="")
 		print("%.4f" % vector[i], end="")
 		print(" ", end="")
	print("\n")


def getPresentMinValue(position , functionCode):
	val = 0.0
	for i in range(len(position)):
		xi = position[i]

		if functionCode == "1":
			tempVal = (xi*math.sin(xi)) + (0.1*xi)
			if tempVal < 0.0:
				tempVal = tempVal*-1
			val += tempVal

		if functionCode == "2":
			val += (xi*xi) + (4*xi) +2

		if functionCode == "5":
			val += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10

		if functionCode == "3":
			part1 = math.sqrt(abs(xi + 2/2 + 47))
			part2 = math.sqrt(abs(2 - (xi+47) ) )

			val += -(xi + 47)*math.sin(part1) -2*math.sin(part2)

		if functionCode == "4":
			val += (xi*xi) + (4*xi) +2

	return val

class Particle:
	def __init__(self, variables, minx, maxx, seed , functionCode):
		self.rnd = random.Random(seed)
		self.position = [random.randrange(minx,maxx) for i in range(variables)]
		self.velocity = [0.0 for i in range(variables)]
		self.best_part_pos = [random.randrange(minx,maxx) for i in range(variables)]

		for i in range(variables):
			self.position[i] = ((maxx - minx) * self.rnd.random() + minx)
			self.velocity[i] = ((maxx - minx) * self.rnd.random() + minx)

		self.error = getPresentMinValue(self.position , functionCode)
		self.best_part_pos = copy.copy(self.position) 
		self.best_part_err = self.error

def Solve(max_ittrations, n, variables, minx, maxx , functionCode):

	ittrList = []
	json = '{"length":' + str(max_ittrations) + ','
	oFunctionCalledCount = 0
	rnd = random.Random(0)
	swarm = [Particle(variables, minx, maxx, i , functionCode) for i in range(n)] 

	best_swarm_pos = [0.0 for i in range(variables)]
	best_swarm_err = sys.float_info.max
	for i in range(n):
		if swarm[i].error < best_swarm_err:
			best_swarm_err = swarm[i].error
			best_swarm_pos = copy.copy(swarm[i].position) 

	ittration = 0
	w = 0.729
	c1 = 1.49445
	c2 = 1.49445

	while ittration < max_ittrations:
    
		if ittration >= 0:

			bestSolForIttration = "%.3f" % best_swarm_err

			#if ittration == max_ittrations - 1:
			#	json = json + '"' + str(ittration) +'"' + ':' +'{"ittration":' + str(ittration) + ', "bestSolutionForIteration":' + str(bestSolForIttration) + "}"
			#else:
			#	json = json + '"' + str(ittration) +'"' + ':' +'{"ittration":' + str(ittration) + ', "bestSolutionForIteration":' + str(bestSolForIttration) + "},"

			data = {}
			data['ittration'] = str(ittration)
			data['bestSolForIttration'] = str(bestSolForIttration)
			ittrList.append(data)
			print("ittration = " + str(ittration) + " best solution = %.3f" % best_swarm_err)

		for i in range(n):
      
			for k in range(variables): 
				r1 = rnd.random() 
				r2 = rnd.random()
    
				swarm[i].velocity[k] = ( (w * swarm[i].velocity[k]) + (c1 * r1 * (swarm[i].best_part_pos[k] - swarm[i].position[k])) +  (c2 * r2 * (best_swarm_pos[k] - swarm[i].position[k])) )  

				if swarm[i].velocity[k] < minx:
					swarm[i].velocity[k] = minx
				elif swarm[i].velocity[k] > maxx:
					swarm[i].velocity[k] = maxx

			for k in range(variables): 
				swarm[i].position[k] += swarm[i].velocity[k]
  
			swarm[i].error = getPresentMinValue(swarm[i].position , functionCode)
			json = json + '"' + str(oFunctionCalledCount) +'"' + ':' +'{"oFunctionCalledCount":' + str(oFunctionCalledCount) + ', "bestSolutionForIteration":' + str(swarm[i].error) + "},"
			oFunctionCalledCount = oFunctionCalledCount + 1
			if swarm[i].error < swarm[i].best_part_err:
				swarm[i].best_part_err = swarm[i].error
				swarm[i].best_part_pos = copy.copy(swarm[i].position)

			if swarm[i].error < best_swarm_err:
				best_swarm_err = swarm[i].error
				best_swarm_pos = copy.copy(swarm[i].position)

		printBestSolutionByPso(best_swarm_pos)
    
		ittration += 1
	json = json + '"999999999999":{"test":"data"}}'
	finalData = {}
	finalData['best'] = best_swarm_pos
	finalData['report'] = json
	return finalData






