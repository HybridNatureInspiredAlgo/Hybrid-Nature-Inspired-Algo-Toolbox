import math


#multimodal function
def ackley(params):
	#fetching parameters
	if params['a']:
		a = int(params['a'])
	else:
		a = int(20)		#recommended value
	if params['b']:
		b = int(params['b'])
	else:
		b = float(0.2)	#recommended value
	if params['c']:
		c = int(params['c'])
	else:
		c = 2*math.pi

	if params['d']:
		d = int(params['d'])
	else:
		d = 2	#not recommended but just to prevent code from breakdown

	x = params['sol']

	part1 = float(0)
	part2 = float(0)

	for i in range(d):
		part1 = part1 + x[i]*x[i]
		part2 = part2 + math.cos(c*x[i])

	part1 = part1/d
	part2 = part2/d

	fun = -1*a*math.exp(-1*b*math.sqrt(part1)) - math.exp(part2) + a + math.exp(1)

	return fun


# 2-D function:
def cross_in_tray(params):

	x = params['sol']

	part1 = math.sqrt(x[0]*x[0]+x[1]*x[1])/math.pi
	part2 = abs(math.sin(x[0])*math.sin(x[1]*math.exp(abs(100-part1)))) + 1
	part3 = -0.0001*math.pow(part2,0.1)

	return part3



def egg_holder(params):
	x = params['sol']

	part1 = math.sqrt(abs(x[1] + x[0]/2 + 47))
	part2 = math.sqrt(abs(x[0] - (x[1]+47) ) )

	fun = -(x[1] + 47)*math.sin(part1) -x[0]*math.sin(part2)

	return fun


def levy(params):
	x = params['sol']
	d = params['d']

	part1 = float(0)
	w = float(0)
	wd = float(0)
	wd = 1 + (x[d]-1)/4
	w1 = 1 + (x[0]-1)/4

	for i in range(d-1):
		w = 1 + (x[i]-1)/4
		part1 = part1 + (w-1)*(w-1)*(1 + 10*math.sin(math.pi*w + 1) )

	part2 = float((wd-1)*(wd-1)*(1+math.sin(2*math.pi*wd)*math.sin(2*math.pi*wd)))
	fun = math.sin(math.pi*w1)*math.sin(math.pi*w1) + part1 + part2

	return fun

		
#multimodal funtion
def rastrigin(params):
	d = params['d']
	x = params['sol']
	part1 = float(0)

	for i in range(d):
		part1 = part1 + x[i]*x[i] - 10*math.cos(2*math.pi*x[i])


	fun = 10*d + part1
	return fun

# 2D function
def shubert(params):
	x = params['sol']
	part1 = float(0)
	part2 = float(0)

	for i in range(1,6):
		part1 = part1 + i*math.cos((i+1)*x[0] + i)
		part2 = part2 + i*math.cos((i+1)*x[1] + i)

	fun = part1 + part2
	return fun


def sphere(params):
	d = params['d']
	x = params['sol']
	fun = float(0)
	for i in range(d):
		fun = fun + x[i]*x[i]

	return fun

def matyas(params):
	x = params['sol']
	fun = float(0)

	fun = 0.26*(x[0]*x[0] + x[1]*x[1]) - 0.48*x[0]*x[1]
	return fun

#multimodal function
def rosenbrock(params):
	d = params['d']
	x = params['sol']

	fun = float(0)

	for i in range(d-1):
		fun = fun + 100*(x[i+1]-x[i]*x[i])*(x[i+1]-x[i]*x[i]) + (x[i]-1)*(x[i]-1)
		return fun

#2D function
def easom(params):
	x = params['sol']

	fun = float(0)

	fun = -math.cos(x[0])*math.cos(x[1])*math.exp(-(x[0]-math.pi)*(x[0]-math.pi) - (x[1]-math.pi)*(x[1]-math.pi))
	return fun

#multimodal function
def styblinski_tang(params):
	d = params['d']
	x = params['sol']

	fun = float(0)

	for i in range(d):
		fun = fun + math.pow(x[i],4) - 16*x[i]*x[i] + 5*x[i]

	fun = fun/2
	return fun



def function(index,params):
	if index==1:
		return ackley(params)

	elif index==2:
		return cross_in_tray(params)

	elif index==3:
		return egg_holder(params)

	elif index==4:
		return levy(params)

	elif index==5:
		return rastrigin(params)

	elif index==6:
		return shubert(params)

	elif index==7:
		return sphere(params)

	elif index==8:
		return matyas(params)

	elif index==9:
		return rosenbrock(params)

	elif index==10:
		return easom(params)

	elif index==11:
		return styblinski_tang(params)


def test():
	return "haha"


