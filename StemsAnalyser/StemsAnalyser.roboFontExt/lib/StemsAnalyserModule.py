import math

def direction(point1, point2):
	direction_x = 4
	direction_y = 4
	if point1.x < point2.x:
		# Direction is RIGHT
		direction_x = 1
	elif point1.x > point2.x:
		# Direction is LEFT
		direction_x = -1
	else:
		# Direction is NONE
		direction_x = 4
		
	if point1.y < point2.y:
		# Direction is UP
		direction_y = 1
	elif point1.y > point2.y:
		# Direction is DOWN
		direction_y = -1
	else:
		# Direction is NONE
		direction_y = 4
	return (direction_x, direction_y)


def rotated(point, angle):
	x = point.x
	y = point.y
	angle = (math.radians(angle))
	cosa = math.cos(angle)
	sina = math.sin(angle)
	rotatedPoint_x = int(cosa*x - sina*y)
	rotatedPoint_y = int(sina*x + cosa*y)
	return (rotatedPoint_x, rotatedPoint_y)
	
	
def angle(point1, point2):
	return math.atan2(point2.y - point1.y, point2.x - point1.x) / math.pi * 180
	
def shearFactor(angle):
	# find the shearFactor r with a given angle
	r = math.tan(math.radians(angle))
	return r

def distance(point1, point2):
	return (abs(point1.x - point2.x), abs(point1.y - point2.y))
	
def hypothenuse(point1, point2):
	return math.sqrt(distance(point1, point2)[0]*distance(point1, point2)[0] + distance(point1, point2)[1]*distance(point1, point2)[1])

def closeAngle(angle1, angle2):
	diff = angle1 - angle2
	while diff >= 90:
		diff -= 180
	while diff < -90:
		diff += 180
	return (abs(diff)<5)

def approxEqual(a1, a2):
	#return abs(a1 - a2) < 10*(abs(a1)/100)
	return ( abs(a1 - a2) <= 10*(abs(a1)/100) )

def opposite(direction1, direction2):
	isOpposite = False
	LR1 = direction1[0]
	UD1 = direction1[1]
	LR2 = direction2[0]
	UD2 = direction2[1]
	if LR1 + LR2 == 0:
		isOpposite = True
	if UD1 + UD2 == 0:
		isOpposite = True
	return isOpposite
	
def isVertical(vector):
	vector = abs(vector)
	if ((65 < vector) and (vector < 115)):
		return True
	else:
		return False
	
def isHorizontal(vector):
	vector = abs(vector)
	if ((0 <= vector) and (vector <= 45)) or ((135 <= vector) and (vector <= 180)):
		return True
	else:
		return False

#True si il existe un element de la liste l pour lequel la fonction p renvoi True (on dit que le predicat p est vrai sur cet element)
def exists(l, p):
	for e in l:
		if p(e):
			return True
	return False

def sheared(point, angle):
	r = shearFactor(angle)
	return (point.x + r*point.y, point.y)

def roundbase(x, base):
	return int(base * round(float(x)/base))
	
def compare((k1,v1),(k2,v2)):
	return v2 - v1

######