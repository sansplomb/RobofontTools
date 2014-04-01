from mojo.events import *
from mojo.drawingTools import *
from vanilla import *
from AppKit import *

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
	return (abs(a1 - a2) < 10)

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
	if ((45 < vector) and (vector < 135)):
		return True
	else:
		return False
	
def isHorizontal(vector):
	vector = abs(vector)
	if ((0 <= vector) and (vector <= 45)) or ((135 <= vector) and (vector <= 180)):
		return True
	else:
		return False

#Ça répond True si il existe un element de la liste l pour lequel la fonction p renvoi True (on dit que le predicat p est vrai sur cet element)
def exists(l, p):
	for e in l:
		if p(e):
			return True
	return False

def sheared(point, angle):
	r = shearFactor(angle)
	return (point.x + r*point.y, point.y)
	
##################

def make_hPointsList(g):
	contoursList = []
	hPointsList = []
	for i in range(len(g)):
		pointsList = []
		for j in g[i].points:
			pointsList.append(j)
		contoursList.append(pointsList)

	for contour_index in range(len(contoursList)):
		for point_index in range(len(contoursList[contour_index])):
			currentPoint = contoursList[contour_index][point_index]
			if point_index == 0:
				prevPoint = contoursList[contour_index][len(contoursList[contour_index])-1]
			else:
				prevPoint = contoursList[contour_index][point_index-1]
			if point_index == len(contoursList[contour_index]) -1:
				nextPoint = contoursList[contour_index][0]
			else:
				nextPoint = contoursList[contour_index][point_index+1]
			
			if currentPoint.type != 'offCurve':
				directionIN = direction(prevPoint, currentPoint)
				directionOUT = direction(currentPoint, nextPoint)
				vectorIN = angle(prevPoint, currentPoint)
				vectorOUT = angle(currentPoint, nextPoint)
				
				hPoint = (currentPoint, contour_index, point_index, directionIN, directionOUT, vectorIN, vectorOUT)
				hPointsList.append(hPoint)
	return hPointsList
	
def getColor(point1, point2, g):
	hasSomeBlack = False
	hasSomeWhite = False
	color = ''
	if abs(point2.x - point1.x) < maxStemX or abs(point2.y - point1.y) < maxStemY:
		hypothLength = int(hypothenuse(point1, point2))
		for j in range(1, hypothLength-1):
			cp_x = point1.x + ((j)/hypothLength)*(point2.x - point1.x)
			cp_y = point1.y + ((j)/hypothLength)*(point2.y - point1.y) 
			if g.pointInside((cp_x, cp_y)):
				hasSomeBlack = True
			else:
				hasSomeWhite = True
			if hasSomeBlack and hasSomeWhite:
				break
			
	if hasSomeBlack and hasSomeWhite:	
		color = 'Gray'
	elif hasSomeBlack:
		color = 'Black'
	else:
		color = 'White'
	return color

def makeStemsList(g_hPoints, g, italicAngle):
	stemsListX_temp = []
	stemsListY_temp = []
	stemsListX = []
	stemsListY = []	
	for source_hPoint in range(len(g_hPoints)):
		for target_hPoint in range(len(g_hPoints)):
			sourcePoint = g_hPoints[source_hPoint][0]
			targetPoint = g_hPoints[target_hPoint][0]
			directionIn_source = g_hPoints[source_hPoint][3]
			directionOut_source = g_hPoints[source_hPoint][4]
			directionIn_target = g_hPoints[target_hPoint][3]
			directionOut_target = g_hPoints[target_hPoint][4]
			angleIn_source =  g_hPoints[source_hPoint][5]
			angleOut_source = g_hPoints[source_hPoint][6]
			angleIn_target =  g_hPoints[target_hPoint][5]
			angleOut_target = g_hPoints[target_hPoint][6]
			color = getColor(sourcePoint, targetPoint, g)
			if color == 'Black':
				c_distance = distance(sourcePoint, targetPoint)
				stem = (sourcePoint, targetPoint, c_distance)
				hypoth = hypothenuse(sourcePoint, targetPoint)
				## if Source and Target are almost aligned
				if closeAngle(angleIn_source, angleIn_target) or closeAngle(angleOut_source, angleOut_target) or closeAngle(angleIn_source, angleOut_target) or closeAngle(angleOut_source, angleIn_target):
					## if Source and Target have opposite direction
					if opposite(directionIn_source, directionIn_target) or opposite(directionIn_source, directionOut_target) or opposite(directionOut_source, directionIn_target):
						
						## if they are horizontal, treat the stem on the Y axis
						if (isHorizontal(angleIn_source) or isHorizontal(angleOut_source)) and (isHorizontal(angleIn_target) or isHorizontal(angleOut_target)):
							if (minStemY < c_distance[1] < maxStemY) and (minStemY <= hypoth <= maxStemY):
								stemsListY_temp.append(stem)
								
						## if they are vertical, treat the stem on the X axis		
						if (isVertical(angleIn_source) or isVertical(angleOut_source)) and (isVertical(angleIn_target) or isVertical(angleOut_target)):
							
							if (minStemX <= c_distance[0] <= maxStemX) and (minStemX <= hypoth <= maxStemX):
								stemsListX_temp.append(stem)
	# avoid duplicates, filters temporary stems
	yList = []
	for stem in stemsListY_temp:
		if stem[0].y not in yList or stem[1].y not in yList:
			stemsListY.append(stem)
			yList.append(stem[0].y)
			yList.append(stem[1].y)

	xList = []
	for stem in stemsListX_temp:
		(preRot0x, preRot0y) = rotated(stem[0], italicAngle)
		(preRot1x, preRot1y) = rotated(stem[1], italicAngle)
		def pred0(x):
			#print preRot0x, x
			return approxEqual(preRot0x, x)
		def pred1(x):
			#print preRot1x, x
			return approxEqual(preRot1x, x)
		if not exists(xList,pred0) or not exists(xList,pred1):
			stemsListX.append(stem)
			xList.append(preRot0x)
			xList.append(preRot1x)
	
	return (stemsListX, stemsListY)
	
################
minStemX = 20
minStemY = 20
maxStemX = 400
maxStemY = 400

f = CurrentFont()
if f.info.italicAngle != None:
	ital = - f.info.italicAngle
else:
	ital = 0
	
g = f['o']
if not g:
	print "WARNING: glyph 'o' missing"
o_hPoints = make_hPointsList(g)
(o_stemsListX, o_stemsListY) = makeStemsList(o_hPoints, g, ital)

g = f['O']
if not g:
	print "WARNING: glyph 'O' missing"
O_hPoints = make_hPointsList(g)
(O_stemsListX, O_stemsListY) = makeStemsList(O_hPoints, g, ital)

Xs = []
for i in O_stemsListX:
	Xs.append(i[2][0])
maxX = max(Xs)

Ys = []
for i in o_stemsListY:
	Ys.append(i[2][1])
minY = min(Ys)


minStemX = minY - 20*(minY/100)
minStemY = minY - 20*(minY/100)

maxStemX = maxX + 20*(maxX/100)
maxStemY = maxX + 20*(maxX/100)

print 'minX', minStemX, 'maxX', maxStemX
print 'minY', minStemY, 'maxY', maxStemY		
################

class WindowController(object):
	
	def __init__(self):
		self.w = FloatingWindow((200, 100), "Detect Stems")
		self.w.startButton = Button((10, 70, 90, -10), "Start", callback=self.startButtonCallBack)
		self.w.stopButton = Button((110, 70, -10, -10), "Stop", callback=self.stopButtonCallBack)
		self.w.open()

		# create a background color
		self.backgroundColorX = NSColor.redColor()
		self.backgroundColorY = NSColor.blackColor()
		# create a background stroke color
		self.backgroundStrokeColor = NSColor.whiteColor()
		# create a stroke color
		self.strokeColorX = NSColor.redColor()
		self.strokeColorY = NSColor.blackColor()
		# setting text attributes
		self.attributes = attributes = {
			NSFontAttributeName : NSFont.boldSystemFontOfSize_(9),
			NSForegroundColorAttributeName : NSColor.whiteColor(),
			}
	
	def draw(self, notification):
		glyph = notification["glyph"]
		if self.g == glyph:
			view = notification["view"]
			scale = notification["scale"] 
			pathX = NSBezierPath.bezierPath()
			pathY = NSBezierPath.bezierPath()
			
			valuesListX = []
			for stem in self.stemsListX:
				startPoint_x = stem[0].x
				startPoint_y = stem[0].y
				endPoint_x = stem[1].x
				endPoint_y = stem[1].y
				length = float(stem[2][0])
				pathX.moveToPoint_((startPoint_x, startPoint_y))
				pathX.lineToPoint_((endPoint_x, endPoint_y))
				center_x = startPoint_x + (endPoint_x - startPoint_x) * 0.5
				center_y = startPoint_y + (endPoint_y - startPoint_y) * 0.5
				valuesListX.append((center_x, center_y, length))
			# set the stroke color
			self.strokeColorX.set()
			# set the line width of the path
			pathX.setLineWidth_(scale)
			# stroke the path
			pathX.stroke()
			
			for x, y, lengthValue in valuesListX:
				if lengthValue.is_integer():
					t = "%i"
				else:
					t = "%.2f"
				view._drawTextAtPoint(t % lengthValue, self.attributes, (x, y), drawBackground=True, backgroundColor=self.backgroundColorX, backgroundStrokeColor=self.backgroundStrokeColor)
				
			valuesListY = []
			for stem in self.stemsListY:
				startPoint_x = stem[0].x
				startPoint_y = stem[0].y
				endPoint_x = stem[1].x
				endPoint_y = stem[1].y
				length = float(stem[2][1])
				pathY.moveToPoint_((startPoint_x, startPoint_y))
				pathY.lineToPoint_((endPoint_x, endPoint_y))
				center_x = startPoint_x + (endPoint_x - startPoint_x) * 0.5
				center_y = startPoint_y + (endPoint_y - startPoint_y) * 0.5
				valuesListY.append((center_x, center_y, length))
			# set the stroke color
			self.strokeColorY.set()
			# set the line width of the path
			pathY.setLineWidth_(scale)
			# stroke the path
			pathY.stroke()
			
			for x, y, lengthValue in valuesListY:
				if lengthValue.is_integer():
					t = "%i"
				else:
					t = "%.2f"
				view._drawTextAtPoint(t % lengthValue, self.attributes, (x, y), drawBackground=True, backgroundColor=self.backgroundColorY, backgroundStrokeColor=self.backgroundStrokeColor)
	
	def startButtonCallBack(self, sender):
		self.f = CurrentFont()
		if self.f.info.italicAngle != None:
			self.ital = - self.f.info.italicAngle
		else:
			self.ital = 0
		self.g = CurrentGlyph()
		self.g_hPoints = make_hPointsList(self.g)
		(self.stemsListX, self.stemsListY) = makeStemsList(self.g_hPoints, self.g, self.ital)
		addObserver(self, "draw", "draw")
		addObserver(self, "draw", "drawBackground")	
	
	def stopButtonCallBack(self, sender):
		removeObserver(self, "draw")	
		removeObserver(self, "drawBackground")
		self.w.close()


		
WindowController()
		