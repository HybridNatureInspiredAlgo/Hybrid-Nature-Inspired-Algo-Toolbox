from django.shortcuts import render
from django.http import JsonResponse
import json
from django.http import HttpResponse
# Create your views here.
import random
import math
from NatureInspiredHybridAlgoToolbox import benchmark_functions

class BeeColony:
	'functionality of bee colony algorithm'
	def __init__(self,input_data):
		#Control Parameters of ABC algorithm
		self.NP = int(input_data['np'])			# Colony size (employed bees + onlooker bees)
		self.FoodNumber = int(self.NP/2)	# Food sorces = half the size of the colony
		self.limit = int(input_data['limit'])		# A food source which could not be improved through "limit" trials is abandoned by its employed bee
		self.maxCycle = int(input_data['maxCycle'])	# The number of cycles for foraging {a stopping criteria

		#Problem specific variables
		self.D = int(input_data['dimensions'])			#The number of parameters of the problem to be optimized
		self.lb = float(input_data['lower_bound'])		#lower bound of the parameters.
		self.ub = float(input_data['upper_bound'])		#upper bound of the parameters. lb and ub can be defined as arrays for the problems of which parameters have different bounds

		self.runtime = int(input_data['max_runtime'])		#Algorithm can be run many times in order to see its robustness
		self.function_number = int(input_data['function']) 	#The number corresponding to functions as given in benchmark_functions
		self.dizi1 = [0]*10

		self.objective_function_count = int(0)
		self.output = {}

		self.Foods = [[float(0) for x in range(self.D)] for y in range(self.FoodNumber)]
		# Foods is the population of food sources. Each row of Foods matrix is a vector holding D parameters to be optimized. The number of rows of Foods matrix equals to the FoodNumber
		self.f = [float(0) for x in range(self.FoodNumber)]
		#f is a vector holding objective function values associated with food sources 
		self.fitness = [float(0) for x in range(self.FoodNumber)]
		#fitness is a vector holding fitness (quality) values associated with food sources
		self.trial = [float(0) for x in range(self.FoodNumber)]
		#trial is a vector holding trial numbers through which solutions can not be improved
		self.prob = [float(0) for x in range(self.FoodNumber)]
		#prob is a vector holding probabilities of food sources (solutions) to be chosen
		self.solution = [float(0) for x in range(self.D)]
		#New solution (neighbour) produced by v_{ij}=x_{ij}+\phi_{ij}*(x_{kj}-x_{ij}) j is a randomly chosen parameter and k is a randomlu chosen solution different from i

		self.ObjValSol = float(0)	#Objective function value of new solution
		self.FitnessSol = float(0) 	#Fitness value of new solution
		self.neighbour = int(0)		#neighbour corresponds to k in equation v_{ij}=x_{ij}+\phi_{ij}*(x_{kj}-x_{ij})
		self.param2change = int(0)	#param2change corrresponds to j
		self.GlobalMin = float(0)	#Optimum solution obtained by ABC algorithm
		self.GlobalParams = [float(0) for x in range(self.D)]	#Parameters of the optimum solution
		self.GlobalMins = [float(0) for x in range(self.runtime)]		#GlobalMins holds the GlobalMin of each run in multiple runs
		self.r = float(0)										# A random number in the range [0,1


	#a function pointer returning double and taking a D-dimensional array as argument 
	#If your function takes additional arguments then change function pointer definition and lines calling "...=function(solution);" in the code

	#fitness function
	def CalculateFitness(self,fun):
		result = float(0);

		if fun>=0:
			result = 1/(fun + 1)
		else:
			result = 1 + abs(fun)

		return result

	#The best food source is memorized
	def MemorizeBestSource(self):
		i = int(0)
		j = int(0)

		for i in range(self.FoodNumber):
			if self.f[i]<self.GlobalMin:
				self.GlobalMin = self.f[i]
				for j in range(self.D):
					self.GlobalParams[j] = self.Foods[i][j]


	#Variables are initialized in the range [lb,ub]. If each parameter has different range, use arrays lb[j], ub[j] instead of lb and ub 
	#Counters of food sources are also initialized in this function


	def init(self,index):
		j = int(0)
		for j in range(self.D):
			self.r = float(float(random.random()*32767)/(float(32768)))
			self.Foods[index][j] = self.r*(self.ub-self.lb)+self.lb
			self.solution[j] = self.Foods[index][j]
			self.f[index] = self.calculateFunction(self.solution,self.function_number)
			self.fitness[index] = self.CalculateFitness(self.f[index])
			self.trial[index] = 0


	#All food sources are initialized 
	def initial(self):
		i = int(0)
		for i in range(self.FoodNumber):
			init = i
		self.GlobalMin = self.f[0]
		for i in range(self.D):
			self.GlobalParams[i] = self.Foods[0][i]

	def SendEmployedBees(self):
		i = int(0)
		j = int(0)
		#Employed Bee Phase		
		for i in range(self.FoodNumber):
		#The parameter to be changed is determined randomly
			self.r = float(float(random.random()*32767)/(float(32768)))
			self.param2change = int(self.r*self.D)

			#A randomly chosen solution is used in producing a mutant solution of the solution i
			self.r = float(float(random.random()*32767)/(float(32768)))
			self.neighbour = int(self.r*self.FoodNumber)

			for j in range(self.D):
				self.solution[j] = self.Foods[i][j]

			#v_{ij}=x_{ij}+\phi_{ij}*(x_{kj}-x_{ij})
			self.r = float(float(random.random()*32767)/(float(32768)))
			self.solution[self.param2change] = self.Foods[i][self.param2change]+(self.Foods[i][self.param2change] - self.Foods[self.neighbour][self.param2change])*(self.r - 0.5)*2	
			#if generated parameter value is out of boundaries, it is shifted onto the boundaries
			if self.solution[self.param2change]<self.lb:
				self.solution[self.param2change]=self.lb
			if self.solution[self.param2change]>self.ub:
				self.solution[self.param2change] = self.ub

			self.ObjValSol=self.calculateFunction(self.solution,self.function_number);
			self.FitnessSol=self.CalculateFitness(self.ObjValSol);

			#a greedy selection is applied between the current solution i and its mutant
			if self.FitnessSol>self.fitness[i]:
				#If the mutant solution is better than the current solution i, replace the solution with the mutant and reset the trial counter of solution i
				self.trial[i]=0
				for j in range(self.D):
					self.Foods[i][j] = self.solution[j]
					self.f[i] = self.ObjValSol
					self.fitness[i] = self.FitnessSol
			else:
				#if the solution i can not be improved, increase its trial counter
				self.trial[i] = self.trial[i]+1


		#end of employed bee phase


	#A food source is chosen with the probability which is proportioal to its quality*/
	#Different schemes can be used to calculate the probability values*/
	#For example prob(i)=fitness(i)/sum(fitness)*/
	#or in a way used in the metot below prob(i)=a*fitness(i)/max(fitness)+b*/
	#probability values are calculated by using fitness values and normalized by dividing maximum fitness value*/

	def CalculateProbabilities(self):
		i = int(0)
		
		maxfit = self.fitness[0]

		for i in range(1,self.FoodNumber):
			if self.fitness[i]>maxfit:
				maxfit = self.fitness[i]

		for i in range(self.FoodNumber):
			self.prob[i] = (0.9*float(self.fitness[i]/maxfit)) + 0.1


	def SendOnLookerBees(self):
		i = int(0)
		j = int(0)
		t = int(0)
		#onlooker Bee Phase
		while t<self.FoodNumber:
			self.r = float(float(random.random()*32767)/(float(32768)))
			if self.r < self.prob[i]: #choose a food source depending on its probability to be chose
				t = t+1

				#The parameter to be changed is determined randomly
				self.r = float(float(random.random()*32767)/(float(32768)))
				self.param2change = int(self.r*self.D)

				#A randomly chosen solution is used in producing a mutant solution of the solution i
				self.r = float(float(random.random()*32767)/(float(32768)))
				self.neighbour = int(self.r*self.FoodNumber)

				#Randomly selected solution must be different from the solution i
				while self.neighbour == i:
					#System.out.println(Math.random()*32767+"  "+32767);
					self.r = float(float(random.random()*32767)/(float(32768)))
					self.neighbour = int(self.r*self.FoodNumber)


				for j in range(self.D):
					self.solution[j] = self.Foods[i][j]

				#v_{ij}=x_{ij}+\phi_{ij}*(x_{kj}-x_{ij}) 
				self.r = float(float(random.random()*32767)/(float(32768)))
				self.solution[self.param2change] = self.Foods[i][self.param2change] + (self.Foods[i][self.param2change] - self.Foods[self.neighbour][self.param2change])*(self.r - 0.5)*2

				#if generated parameter value is out of boundaries, it is shifted onto the boundaries
				if self.solution[self.param2change] < self.lb:
					self.solution[self.param2change] = self.lb

				if self.solution[self.param2change] > self.ub:
					self.solution[self.param2change] = self.ub

				self.ObjValSol = self.calculateFunction(self.solution,self.function_number)
				self.FitnessSol = self.CalculateFitness(self.ObjValSol)

				#a greedy selection is applied between the current solution i and its mutant
				if self.FitnessSol > self.fitness[i]:
					#If the mutant solution is better than the current solution i, replace the solution with the mutant and reset the trial counter of solution i
					self.trial[i] = 0

					for j in range(self.D):
						self.Foods[i][j] = self.solution[j]

					self.f[i] = self.ObjValSol
					self.fitness[i] = self.FitnessSol
				else:
					#if the solution i can not be improved, increase its trial counter
					self.trial[i] = self.trial[i] + 1

			i = i + 1
			if i==self.FoodNumber:
				i = 0

	#determine the food sources whose trial counter exceeds the "limit" value. In Basic ABC, only one scout is allowed to occur in each cycle
	def SendScoutBees(self):
		maxtrialindex = int(0)
		i = int(0)

		for i in range(1,self.FoodNumber):
			if(self.trial[i] > self.trial[maxtrialindex]):
				maxtrialindex = i

		if self.trial[maxtrialindex] >= self.limit:
			self.init(maxtrialindex)


	def calculateFunction(self,sol,num):
		params={"sol":sol,"d":self.D}
		value = float(0)
		value = benchmark_functions.function(num,params)
		item = {"bestSolutionForIteration":value}
		self.output[self.objective_function_count] = item
		self.objective_function_count += 1
		return value
		#return self.myown(sol);

	def sphere(self,sol):
		j = int(0)
		top = float(0)

		for j in range(self.D):
			top = top + sol[j]*sol[j]

		return top


	def Rosenbrock(self,sol):
		j = int(j)
		top = float(0)

		for j in range(D-1):
			top = top + 100*math.pow((sol[j+1]-math.pow((sol[j]),float(2) )), float(2)+ math.pow((sol[j]-1),float(2)) )

		return top


	def Griewank(self,sol):
		j = int(0)
		top1 = float(0)
		top2 = float(1)
		top = float(0)

		for j in range(self.D):
			top1 = top1 + math.pow(sol[j],float(2))
			top2 = top2 * math.cos((((sol[j])/math.sqrt(float(j+1)))*math.pi)/180)

		top = (1 / float(4000))*top1-top2+1;

		return top

	 
	def  Rastrigin(self,sol):
	 	j = int(0)
	 	top = float(0)

	 	for j in range(self.D):
	 		top = top + math.pow(sol[j],float(2))-10*math.cos(2*math.pi*sol[j])+10
	 		
	 	return top

	def myown(self,sol):
	 	top = float(0)
	 	for j in range(self.D):
	 		top = sol[j]*sol[j] + top

	 	#top = top  - 5
	 	return top


def run(request):
	input_data = {'np':request.GET.get('np'),'limit':100,'maxCycle':request.GET.get('n_gen'),'dimensions':request.GET.get('d'),'lower_bound':request.GET.get('lower'),'upper_bound':request.GET.get('upper'),'max_runtime':30,'function':request.GET.get('function')}

	bee = BeeColony(input_data)
	iterr = int(0)
	run = int(0)
	j = int(0)
	mean = float(0)
	#data = {}
	#item = {}
	for run in range(bee.runtime):
		bee.initial()
		bee.MemorizeBestSource()

		for interr in range(bee.maxCycle):
			bee.SendEmployedBees()
			bee.CalculateProbabilities()
			bee.SendOnLookerBees()
			bee.MemorizeBestSource()
			bee.SendScoutBees()
				
		#for j in range(bee.D):
		#	print("GlobalParam[",(j+1),"]:",bee.GlobalParams[j])

		#print((run+1),".run:",bee.GlobalMin)
		bee.GlobalMins[run] = bee.GlobalMin
		#item["bestSolutionForIteration"] = bee.GlobalMin
		#data[bee.objective_function_count] = item
		mean = mean + bee.GlobalMin

	mean = mean/bee.runtime
	#print("Means  of ",bee.runtime,"runs: ",mean)
	#data["len"] = bee.objective_function_count
	bee.output["length"] = bee.objective_function_count
	#return HttpResponse(mean)

	return HttpResponse(str(json.dumps(bee.output)))

	# return HttpResponse('{"length":4,"0":{"bestSolutionForIteration":0.0012},"1":{"bestSolutionForIteration":0.62}, "2":{"bestSolutionForIteration":0.72},"3":{"bestSolutionForIteration":1.0012} }')




def index(request):

	return render(request,'abc.html')


def search(request):
	for i in details:
		data[i] = request.GET.get(i)
	return HttpResponse(json.dumps(data))
