from mojo.events import addObserver
from mojo.drawingTools import *
from AppKit import *


import math


def getDirection(Point1, Point2):
	directionX = ''
	directionY = ''
	if Point1.x < Point2.x:
		# Direction is RIGHT
		directionX = 1
	elif Point1.x > Point2.x:
		# Direction is LEFT
		directionX = -1
	else:
		# Direction is NONE
		directionX = 4
		
	if Point1.y < Point2.y:
		# Direction is UP
		directionY = 1
	elif Point1.y > Point2.y:
		# Direction is DOWN
		directionY = -1
	else:
		# Direction is NONE
		directionY = 4
	
	return (directionX, directionY)

def gethPointsList(c_glyph):
	contoursList = []
	for i in range(len(c_glyph)):
		pointsList = []
		for j in c_glyph[i].points:
			pointsList.append(j)
		contoursList.append(pointsList)

	hPointsList = []
	for i in range(len(contoursList)):
		for j in range(len(contoursList[i])):
			currentPoint = contoursList[i][j]
			if j == 0:
				prevPoint = contoursList[i][len(contoursList[i])-1]
			else:
				prevPoint = contoursList[i][j-1]
			if j == len(contoursList[i])-1:
				nextPoint = contoursList[i][0]
			else:
				nextPoint = contoursList[i][j+1]
		
			if currentPoint.type != 'offCurve':
				currentDirectionOUT = getDirection(currentPoint, nextPoint)
				currentDirectionIN = getDirection(prevPoint, currentPoint)
				isAlignedOUT = isAlignedCheck(currentPoint, nextPoint)
				isAlignedIN = isAlignedCheck(prevPoint, currentPoint)

				current_hPoint = (currentPoint, currentDirectionOUT, currentDirectionIN, isAlignedOUT, isAlignedIN, prevPoint, nextPoint)
				hPointsList.append(current_hPoint)
	return hPointsList
	
def getDistance((x1, y1), (x2, y2)):
	return (abs(x1-x2), abs(y1-y2))


def isOppositeCheck((LR1, UD1), (LR2, UD2)):
	isOpposite = False
	if LR1 + LR2 == 0:
		isOpposite = True
	if UD1 + UD2 == 0:
		isOpposite = True
	return isOpposite

def isSameCheck((LR1, UD1), (LR2, UD2)):
	isSame = False
	if abs(LR1 + LR2) == 2:
		isSame = True
	if abs(UD1 + UD2) == 2:
		isSame = True
	return isSame
	
def getMinHypothIndex(hypothList):
	minHypoth = min(hypothList)
	index = 0
	for i in range(len(hypothList)-1):
		if hypothList[i] == minHypoth:
			index = i
	return index

def getHighest(valuesDict):
	highest = 1
	value = 0
	if len(valuesDict.keys()) != 0:
		value = valuesDict.keys()[0]
		for i in valuesDict.keys():	
			if valuesDict[i] > highest:
				highest = valuesDict[i]
				value = i
		del valuesDict[value]	
	return value, highest
	
		
def refineValues(ValuesList, minStem, maxStem):
	refinedList = []
	for i in ValuesList:
		if maxStem < i :
			continue
		if i < minStem:
			continue
		elif i != 0:
			refinedList.append(i)
	return refinedList
	
	
def parseGlyph(c_glyph, hPointsList, xStems, yStems):
	# cette methode est tres lente et n'apporte pas grand chose...
	(xMin, yMin, xMax, yMax) = c_glyph.box
	newStemsXList = []
	newStemsYList = []
	hintsListX = []
	hintsListY = []
	Ysources = []
	Ytargets = []
	Xsources = []
	Xtargets = []
	
	n = len(hPointsList)
	for i in reversed(range(xMin, xMax)):
		for j in range(n):
			for k in range(n):
				sourceP_x = hPointsList[k][0].x
				targetP_x = hPointsList[j][0].x
				for xStem in xStems:
					if sourceP_x == i:
						if getColor(hPointsList[j][0], hPointsList[k][0], c_glyph) == 'Black':
							if hPointsList[j][3] == 'Vertical' and hPointsList[k][3] == 'Vertical' or hPointsList[j][3] == 'Vertical' and hPointsList[k][4] == 'Vertical' or hPointsList[j][4] == 'Vertical' and hPointsList[k][3] == 'Vertical':
								if i - xStem + 25*(xStem/100) <= targetP_x <= i + xStem + 25*(xStem/100) and sourceP_x != targetP_x :
									newStemX = getDistance((sourceP_x, 0), (targetP_x, 0))[0]
									newHint = (hPointsList[j][0], hPointsList[k][0], newStemX)
									if newHint not in hintsListX and targetP_x not in Xtargets and sourceP_x not in Xsources and minStemX < newStemX < maxStemX:
										hintsListX.append(newHint)
										newStemsXList.append(newStemX)
									if sourceP_x not in Xsources:
										Xsources.append(sourceP_x)
									if targetP_x not in Xtargets:
										Xtargets.append(targetP_x)
	# check alignements
	alignedHintsX = []
	for hint in hintsListX:
		for i in range(n):
			c_ip = hPointsList[i][0]
			prev_ip = hPointsList[i][5]
			next_ip = hPointsList[i][6]
			if c_ip == hint[0] or c_ip == hint[1]:
				for j in range(n):
					c_jp = hPointsList[j][0]
					if c_jp.x -5 <= c_ip.x <= c_jp.x +5 and i != j and c_jp != prev_ip and c_jp != next_ip and c_jp.y not in Ysources and c_jp.y not in Ytargets:
						newHint = (c_ip, c_jp, 0)
						alignedHintsX.append(newHint)
						
					

	for i in reversed(range(yMin, yMax)):
		for j in range(n):
			for k in range(n):
				sourceP_y = hPointsList[k][0].y
				targetP_y = hPointsList[j][0].y
				for yStem in yStems:
					if sourceP_y == i:
						color = getColor(hPointsList[j][0], hPointsList[k][0], c_glyph)
						if color == 'Black':
							if hPointsList[j][3] == 'Horizontal' and hPointsList[k][3] == 'Horizontal' or hPointsList[j][3] == 'Horizontal' and hPointsList[k][4] == 'Horizontal' or hPointsList[j][4] == 'Horizontal' and hPointsList[k][3] == 'Horizontal': 
								if i - yStem + 25*(yStem/100) <= targetP_y <= i + yStem + 25*(yStem/100) and sourceP_y != targetP_y :
									newStemY = getDistance((0, sourceP_y), (0, targetP_y))[1]
									newHint = (hPointsList[j][0], hPointsList[k][0], newStemY)
									if newHint not in hintsListY and sourceP_y not in Ysources and sourceP_y not in Ytargets and minStemY < newStemY < maxStemY:	
										hintsListY.append(newHint)
										newStemsYList.append(newStemY)
									if sourceP_y not in Ysources:
										Ysources.append(sourceP_y)
									if targetP_y not in Ytargets:
										Ytargets.append(targetP_y)
	# check alignements
	alignedHintsY = []
	for hint in hintsListY:
		for i in range(n):
			c_ip = hPointsList[i][0]
			prev_ip = hPointsList[i][5]
			next_ip = hPointsList[i][6]
			if c_ip == hint[0] or c_ip == hint[1]:
				for j in range(n):
					c_jp = hPointsList[j][0]
					if c_jp.y -5 <= c_ip.y <= c_jp.y +5 and i != j and c_jp != prev_ip and c_jp != next_ip and c_jp.x not in Xsources and c_jp.x not in Xtargets:
						newHint = (c_ip, c_jp, 0)
						alignedHintsY.append(newHint)
	
	hintsListX.extend(alignedHintsX)
	hintsListY.extend(alignedHintsY)
	
	print hintsListX, hintsListY											
	return hintsListX, hintsListY
					
		
def getColor(point1, point2, g):
	hasSomeBlack = False
	hasSomeWhite = False
	color = ''
	selectedPoints = []
	for c in g:
		for p in range(len(c.points)):
			if c.points[p].selected:
				selectedPoints.append(c.points[p])
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

def isAlignedCheck(point1, point2):
	isAligned = ''
	if abs(point1.x - point2.x) < 3:
		isAligned = 'Vertical'
	elif abs(point1.y - point2.y) < 3:
		isAligned = 'Horizontal'
	else:
		isAligned = 'Diagonal'
	return isAligned
	
def getDistances(hPointList, c_glyph):
	xCandidatesList = []
	yCandidatesList = []
	n = len(hPointList)
	for i in range(n):	
		hpointDistancesYList = []
		hpointDistancesXList = []
		for j in range(i+1, n):
			isOppositeCurrent = isOppositeCheck(hPointsList[i][1], hPointsList[j][1])
			isOppositePrev = isOppositeCheck(hPointsList[i][2], hPointsList[j][1])
			isSameCurrent = isSameCheck(hPointsList[i][1], hPointsList[j][1])
			isSamePrev = isSameCheck(hPointsList[i][2], hPointsList[j][1])
			currentDistance = getDistance((hPointsList[i][0].x, hPointsList[i][0].y), (hPointsList[j][0].x, hPointsList[j][0].y))
			currentHypoth = math.sqrt(currentDistance[0]*currentDistance[0] + currentDistance[1]*currentDistance[1])
			if currentHypoth > maxStemX or currentHypoth > maxStemY:
				continue
			color = getColor(hPointsList[i][0], hPointsList[j][0], c_glyph)
			if isOppositeCurrent or isOppositePrev:
				if color == 'Black':
					if currentHypoth != 0:
						# if currentPoint has horizontal direction
						if abs(hPointsList[i][1][0]) == 1 or abs(hPointsList[i][2][0]) == 1 :
							if hPointsList[i][3] == 'Horizontal'  or hPointsList[j][3] == 'Horizontal':
								hpointDistancesYList.append((currentDistance, currentHypoth))
							if hPointsList[i][4] == 'Horizontal' or hPointsList[j][4] == 'Horizontal':
								hpointDistancesYList.append((currentDistance, currentHypoth))
						# if currentPoint has vertical direction
						if abs(hPointsList[i][1][1]) == 1 or abs(hPointsList[i][2][1]) == 1 :
							if hPointsList[i][3] == 'Vertical' or hPointsList[j][3] == 'Vertical':
								hpointDistancesXList.append((currentDistance, currentHypoth))
							if hPointsList[i][4] == 'Vertical' or hPointsList[j][4] == 'Vertical':
								hpointDistancesXList.append((currentDistance, currentHypoth))
						# if currentPoint has diagonal direction
						if abs(hPointsList[i][1][1]) == 1 and abs(hPointsList[i][1][0]) == 1 or abs(hPointsList[i][2][1]) == 1 and abs(hPointsList[i][2][0]) == 1:
							if hPointsList[i][3] == 'Diagonal' or hPointsList[j][3] == 'Diagonal':
								hpointDistancesXList.append((currentDistance, currentHypoth))
								hpointDistancesYList.append((currentDistance, currentHypoth))
							if hPointsList[i][4] == 'Diagonal' or hPointsList[j][4] == 'Diagonal':
								hpointDistancesXList.append((currentDistance, currentHypoth))
								hpointDistancesYList.append((currentDistance, currentHypoth))
			#if isSameCurrent or isSamePrev:
			#	if color == 'White':
			#		if currentHypoth != 0:
			#			# if currentPoint has horizontal direction
			#			if abs(hPointsList[i][1][0]) == 1 or abs(hPointsList[i][2][0]) == 1 :
			#				if hPointsList[i][3] == 'Horizontal' or hPointsList[i][4] == 'Horizontal' and hPointsList[j][3] == 'Horizontal' or hPointsList[j][4] == 'Horizontal':
			#					hpointDistancesYList.append((currentDistance, currentHypoth))
			#			# if currentPoint has vertical direction
			#			if abs(hPointsList[i][1][1]) == 1 or abs(hPointsList[i][2][1]) == 1 :
			#				if hPointsList[i][3] == 'Vertical' or hPointsList[i][4] == 'Vertical' and hPointsList[j][3] == 'Vertical' or hPointsList[j][4] == 'Vertical':
			#					hpointDistancesXList.append((currentDistance, currentHypoth))
					
		# En X
		hPointXdistanceList = []
		hPointHypothList = []
		for j in range(len(hpointDistancesXList)):
			hPointXdistanceList.append(hpointDistancesXList[j][0][0])
			hPointHypothList.append(hpointDistancesXList[j][1])
		if len(hPointHypothList) != 0 :
			minIndex = hPointHypothList.index(min(hPointHypothList))
			xCandidatesList.append(hPointXdistanceList[minIndex])
							
		# En Y
		hPointYdistanceList = []
		hPointHypothList = []
		for j in range(len(hpointDistancesYList)):
			hPointYdistanceList.append(hpointDistancesYList[j][0][1])
			hPointHypothList.append(hpointDistancesYList[j][1])
		if len(hPointHypothList) != 0 :
			minIndex = hPointHypothList.index(min(hPointHypothList))
			yCandidatesList.append(hPointYdistanceList[minIndex])
		
	xCandidatesList.sort()
	xRefinedList = refineValues(xCandidatesList, minStemX, maxStemX)
	
	yCandidatesList.sort()
	yRefinedList = refineValues(yCandidatesList, minStemY, maxStemY)
	
	return (xRefinedList, yRefinedList)
	#return (xCandidatesList, yCandidatesList)

f = CurrentFont()
c_glyph = CurrentGlyph()

minStemX = 20
minStemY = 20
maxStemX = 300
maxStemY = 200
	
hPointsList = gethPointsList(f['O'])
(UC_xStems, UC_yStems) = getDistances(hPointsList, f['O'])

print 'O x_Stems:', UC_xStems
print 'O y_Stems:', UC_yStems

hPointsList = gethPointsList(f['o'])
(LC_xStems, LC_yStems) = getDistances(hPointsList, f['o'])

print 'o x_Stems:', LC_xStems
print 'o y_Stems:', LC_yStems

	
	
#valuesDict_x = {}
#valuesDict_y = {}

hPointsList = gethPointsList(c_glyph)

if c_glyph.name.isupper():
	(hintsListX, hintsListY) = parseGlyph(c_glyph, hPointsList, UC_xStems, UC_yStems)
else:
	(hintsListX, hintsListY) = parseGlyph(c_glyph, hPointsList, LC_xStems, LC_yStems)
		
class DisplayHintsController(object):
	
	def __init__(self):
		# subscribe to the draw event
		addObserver(self, "draw", "draw")
		addObserver(self, "draw", "drawBackground")

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
		selection = glyph.selection
		if c_glyph == glyph:
			view = notification["view"]
			scale = notification["scale"] 
			pathX = NSBezierPath.bezierPath()
			pathY = NSBezierPath.bezierPath()
			
			valuesList = []
			for hint in hintsListX:
				startPoint_x = hint[0].x
				startPoint_y = hint[0].y
				endPoint_x = hint[1].x
				endPoint_y = hint[1].y
				length = float(hint[2])
				pathX.moveToPoint_((startPoint_x, startPoint_y))
				pathX.lineToPoint_((endPoint_x, endPoint_y))
				center_x = startPoint_x + (endPoint_x - startPoint_x) * 0.5
				center_y = startPoint_y + (endPoint_y - startPoint_y) * 0.5
				valuesList.append((center_x, center_y, length))
			# set the stroke color
			self.strokeColorX.set()
			# set the line width of the path
			pathX.setLineWidth_(scale)
			# stroke the path
			pathX.stroke()
			
			for x, y, lengthValue in valuesList:
				if lengthValue.is_integer():
					t = "%i"
				else:
					t = "%.2f"
				view._drawTextAtPoint(t % lengthValue, self.attributes, (x, y), drawBackground=True, backgroundColor=self.backgroundColorX, backgroundStrokeColor=self.backgroundStrokeColor)
			
			valuesList = []
			for hint in hintsListY:
				startPoint_x = hint[0].x
				startPoint_y = hint[0].y
				endPoint_x = hint[1].x
				endPoint_y = hint[1].y
				length = float(hint[2])
				pathY.moveToPoint_((startPoint_x, startPoint_y))
				pathY.lineToPoint_((endPoint_x, endPoint_y))
				center_x = startPoint_x + (endPoint_x - startPoint_x) * 0.5
				center_y = startPoint_y + (endPoint_y - startPoint_y) * 0.5
				valuesList.append((center_x, center_y, length))
			# set the stroke color
			self.strokeColorY.set()
			# set the line width of the path
			pathY.setLineWidth_(scale)
			# stroke the path
			pathY.stroke()
			
			for x, y, lengthValue in valuesList:
				if lengthValue.is_integer():
					t = "%i"
				else:
					t = "%.2f"
				view._drawTextAtPoint(t % lengthValue, self.attributes, (x, y), drawBackground=True, backgroundColor=self.backgroundColorY, backgroundStrokeColor=self.backgroundStrokeColor)

	 
				
		
		
DisplayHintsController()