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

				current_hPoint = (currentPoint, currentDirectionOUT, currentDirectionIN, isAlignedOUT, isAlignedIN)
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
		elif i != 0 and i not in refinedList:
			refinedList.append(i)
	return refinedList
			
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
	if abs(point1.x - point2.x) < 5:
		isAligned = 'Vertical'
	elif abs(point1.y - point2.y) < 5:
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
								hpointDistancesYList.append((currentDistance, currentHypoth))
						# if currentPoint has vertical direction
						if abs(hPointsList[i][1][1]) == 1 or abs(hPointsList[i][2][1]) == 1 :
								hpointDistancesXList.append((currentDistance, currentHypoth))
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

f = CurrentFont()
c_glyph = CurrentGlyph()

minStemX = 20
minStemY = 20
maxStemX = 600
maxStemY = 400
	
hPointsList = gethPointsList(f['O'])
(UC_xStems, UC_yStems) = getDistances(hPointsList, f['O'])

hPointsList = gethPointsList(f['o'])
(LC_xStems, LC_yStems) = getDistances(hPointsList, f['o'])


if len(UC_xStems) > 1 or len(UC_yStems)> 1 :
	print "warning: uppercase 'O' is asymetrical"
if len(LC_xStems) > 1 or len(LC_yStems)> 1 :
	print "warning: lowercase 'o' is asymetrical"


f.info.postscriptStemSnapH = []
f.info.postscriptStemSnapV = []
f.info.postscriptStemSnapH.append(UC_xStems[0])
f.info.postscriptStemSnapH.append(LC_xStems[0])
f.info.postscriptStemSnapV.append(UC_yStems[0])
f.info.postscriptStemSnapV.append(LC_yStems[0])

print 'PostScriptStemSnapH =', UC_xStems[0], LC_xStems[0]
print 'PostScriptStemSnapV =', UC_yStems[0], LC_yStems[0]
print 'DONE: Stems updated in font info'

