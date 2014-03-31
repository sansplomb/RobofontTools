from mojo.events import *
from mojo.drawingTools import *
from vanilla import *
from AppKit import *

import math

def direction(point1, point2):
	direction_x = ''
	direction_y = ''
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
	
	
def vector(point1, point2):
	return math.atan2(point2.y - point1.y, point2.x - point1.x) / math.pi * 180

def distance(point1, point2):
	return (abs(point1.x - point2.x), abs(point1.y - point2.y))
	
def hypothenuse(point1, point2):
	return math.sqrt(distance(point1, point2)[0]*distance(point1, point2)[0] + distance(point1, point2)[1]*distance(point1, point2)[1])

def approxEqual(vector1, vector2):
	if abs(vector1) - abs(vector2) < 5:
		return True
	else:
		return False

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
				vectorIN = vector(prevPoint, currentPoint)
				vectorOUT = vector(currentPoint, nextPoint)
				
				hPoint = (currentPoint, contour_index, point_index, directionIN, directionOUT, vectorIN, vectorOUT)
				hPointsList.append(hPoint)
	return hPointsList
	
def getColor(point1, point2, g):
	hasSomeBlack = False
	hasSomeWhite = False
	color = ''
	if abs(point2.x - point1.x) < maxStemX or abs(point2.y - point1.y) < maxStemY:
		hypothLength = int(math.sqrt((point2.x - point1.x)*(point2.x - point1.x) + (point2.y - point1.y)*(point2.y - point1.y)))
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

def makeStemsList(g_hPoints, g):
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
			vectorIn_source =  g_hPoints[source_hPoint][5]
			vectorOut_source = g_hPoints[source_hPoint][6]
			vectorIn_target =  g_hPoints[target_hPoint][5]
			vectorOut_target = g_hPoints[target_hPoint][6]
			if approxEqual(vectorIn_source, vectorIn_target) or approxEqual(vectorOut_source, vectorOut_target):
				if opposite(directionIn_source, directionIn_target) or opposite(directionIn_source, directionOut_target):
					c_distance = distance(sourcePoint, targetPoint)
					color = getColor(sourcePoint, targetPoint, g)
					if color == 'Black':
						stem = (sourcePoint, targetPoint, c_distance)
						if (isHorizontal(vectorIn_source) or isHorizontal(vectorOut_source)) and (isHorizontal(vectorIn_target) or isHorizontal(vectorOut_target)):
							if (minStemY < c_distance[1] < maxStemY) :
								stemsListY.append(stem)
						if (isVertical(vectorIn_source) or isVertical(vectorOut_source)) and (isVertical(vectorIn_target) or isVertical(vectorOut_target)):
							if (minStemX < c_distance[0] < maxStemX):
								stemsListX.append(stem)
						## ADD A TEST FOR orientationTargetIn and Out, BOTH SOurce and Target must be 'vertical' or 'horizontal'
	return (stemsListX, stemsListY)
	
################
minStemX = 20
minStemY = 20
maxStemX = 300
maxStemY = 300

f = CurrentFont()

g = f['o']
o_hPoints = make_hPointsList(g )
(o_stemsListX, o_stemsListY) = makeStemsList(o_hPoints, g)

g = f['O']
O_hPoints = make_hPointsList(g )
(O_stemsListX, O_stemsListY) = makeStemsList(O_hPoints, g)



minStemX = o_stemsListY[0][2][1] -20*(o_stemsListY[0][2][1]/100)
minStemY = o_stemsListY[0][2][1] -20*(o_stemsListY[0][2][1]/100)
maxStemX = O_stemsListX[0][2][0] +20*(O_stemsListX[0][2][1]/100)
maxStemY = O_stemsListX[0][2][0] +20*(O_stemsListX[0][2][1]/100)

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
		
		self.g = CurrentGlyph()
		self.g_hPoints = make_hPointsList(self.g)
		(self.stemsListX, self.stemsListY) = makeStemsList(self.g_hPoints, self.g)
		addObserver(self, "draw", "draw")
		addObserver(self, "draw", "drawBackground")	
	
	def stopButtonCallBack(self, sender):
		removeObserver(self, "draw")	
		removeObserver(self, "drawBackground")
		self.w.close()


		
WindowController()
		