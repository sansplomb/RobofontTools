from mojo.events import *
from mojo.drawingTools import *
from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController
from AppKit import *

import math
from StemsAnalyserModule import *

minStemX = 20
minStemY = 20
maxStemX = 400
maxStemY = 400

class WindowController(BaseWindowController):
	
	def __init__(self):
		self.w = FloatingWindow((300, 240), "Stems Analyser")
		self.w.roundTo5CheckBox = CheckBox((10, 20, -10, 20), "Round Values to 5",
						   callback=self.roundTo5CheckBoxCallback, value=True)
		self.w.startButton = Button((10, 50, 170, 30), "Analyse Selected Glyphs", callback=self.startButtonCallBack)
		self.w.xTextBox = TextBox((10, 90, -10, 17), "Horizontal (x):")
		self.w.xValuesEditText = TextBox((10, 110, -10, 22))
		self.w.yTextBox = TextBox((10, 140, -10, 17), "Vertical (y):")
		self.w.yValuesEditText = TextBox((10, 160, -10, 22))
		self.w.applyButton = Button((10, 200, 190, 30), "Copy to PS StemsSnap", callback=self.applyButtonCallBack)
		self.w.stopButton = Button((210, 200, -10, 30), "Close", callback=self.stopButtonCallBack)
		self.w.open()

		self.roundTo5 = 1
		self.stemSnapHList = []
		self.stemSnapVList = []
		
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
	def roundTo5CheckBoxCallback(self, sender):
		self.roundTo5 = sender.get()
		
	def applyButtonCallBack(self, sender):
		f.info.postscriptStemSnapH = self.stemSnapHList
		f.info.postscriptStemSnapV = self.stemSnapVList
		
	def draw(self, notification):
		glyph = notification["glyph"]
		for gStems in self.glyphsStemsList:
			if gStems[0] == glyph.name:
				view = notification["view"]
				scale = notification["scale"] 
				pathX = NSBezierPath.bezierPath()
				pathY = NSBezierPath.bezierPath()
			
				valuesListX = []
				for stem in gStems[1]:
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
				for stem in gStems[2]:
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
		
		self.glyphsStemsList = []
		
		self.w.xValuesEditText.set('')
		self.w.yValuesEditText.set('')
		self.stemsValuesXList = []
		self.stemsValuesYList = []
		self.stemSnapHList = []
		self.stemSnapVList = []
		roundedStemsXList = []
		roundedStemsYList = []
		originalStemsXList = []
		originalStemsYList = []
		
		
		self.f = CurrentFont()
		if self.f.info.italicAngle != None:
			self.ital = - self.f.info.italicAngle
		else:
			self.ital = 0
		self.progress = self.startProgress("Preparing")
		tickCount = 0
		for g in self.f:
			if g.selected:
				tickCount += 1
		
		self.progress.setTickCount(tickCount)
		self.progress.update("Analysing Selected Glyphs")
		for g in self.f:
			if g.selected:
				self.g_hPoints = make_hPointsList(g)
				(self.stemsListX, self.stemsListY) = makeStemsList(self.f, self.g_hPoints, g, self.ital)
				if self.roundTo5 == 1:
					for stem in self.stemsListX:
						roundedStemsXList.append(roundbase(stem[2][0], 5))
					for stem in self.stemsListY:
						roundedStemsYList.append(roundbase(stem[2][1], 5))	
					
					self.stemsValuesXList = roundedStemsXList
					self.stemsValuesYList = roundedStemsYList
					
					self.glyphsStemsList.append((g.name, self.stemsListX, self.stemsListY))
					
				else:
					for stem in self.stemsListX:
						originalStemsXList.append(stem[2][0])
					for stem in self.stemsListY:
						originalStemsYList.append(stem[2][1])
					
					self.stemsValuesXList = originalStemsXList
					self.stemsValuesYList = originalStemsYList
					
					self.glyphsStemsList.append((g.name, self.stemsListX, self.stemsListY))
					
				self.progress.update()
				
				
		self.progress.setTickCount(0)
		self.progress.update("Sorting Values")
		
		valuesXDict = {}
		for StemXValue in self.stemsValuesXList:
			try:
				valuesXDict[StemXValue] += 1
			except KeyError:
				valuesXDict[StemXValue] = 1
		#print 'x',valuesXDict
		
		valuesYDict = {}
		for StemYValue in self.stemsValuesYList:
			try:
				valuesYDict[StemYValue] += 1
			except KeyError:
				valuesYDict[StemYValue] = 1
		#print 'y',valuesYDict
		
		keyValueXList = valuesXDict.items()
		keyValueXList.sort(compare)
		keyValueXList = keyValueXList[:12]
		
		
		for keyValue in keyValueXList:
			self.stemSnapHList.append(keyValue[0])
		#print 'stemSnapH', self.stemSnapHList
		
		stemSnapHText = ''
		for i in self.stemSnapHList:
			stemSnapHText += str(i) + ' '
		self.w.xValuesEditText.set(stemSnapHText)
		
		keyValueYList = valuesYDict.items()
		keyValueYList.sort(compare)
		keyValueYList = keyValueYList[:12]
		

		for keyValue in keyValueYList:
			self.stemSnapVList.append(keyValue[0])
		#print 'stemSnapV', self.stemSnapVList
		
		stemSnapVText = ''
		for i in self.stemSnapVList:
			stemSnapVText += str(i) + ' '
		self.w.yValuesEditText.set(stemSnapVText)
		
		
		addObserver(self, "draw", "draw")
		addObserver(self, "draw", "drawBackground")	
		
		self.progress.close()
		
		
	def stopButtonCallBack(self, sender):
		removeObserver(self, "draw")	
		removeObserver(self, "drawBackground")
		self.w.close()

###################

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

def makeStemsList(f, g_hPoints, g, italicAngle):
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
							if (minStemY < c_distance[1] < maxStemY):
								stemsListY_temp.append(stem)
								
						## if they are vertical, treat the stem on the X axis		
						if (isVertical(angleIn_source) or isVertical(angleOut_source)) and (isVertical(angleIn_target) or isVertical(angleOut_target)):
							
							if (minStemX <= c_distance[0] <= maxStemX):
								stemsListX_temp.append(stem)
	# avoid duplicates, filters temporary stems
	yList = []
	for stem in stemsListY_temp:
		def pred0(y):
			return approxEqual(stem[0].y, y)
		def pred1(y):
			return approxEqual(stem[1].y, y)
		if not exists(yList, pred0) or not exists(yList, pred1):
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

f = CurrentFont()
if f.info.italicAngle != None:
	ital = - f.info.italicAngle
else:
	ital = 0

g = f['o']
if not g:
	print "WARNING: glyph 'o' missing"
o_hPoints = make_hPointsList(g)
(o_stemsListX, o_stemsListY) = makeStemsList(f, o_hPoints, g, ital)

g = f['O']
if not g:
	print "WARNING: glyph 'O' missing"
O_hPoints = make_hPointsList(g)
(O_stemsListX, O_stemsListY) = makeStemsList(f, O_hPoints, g, ital)

Xs = []
for i in O_stemsListX:
	Xs.append(i[2][0])
maxX = max(Xs)

Ys = []
for i in o_stemsListY:
	Ys.append(i[2][1])
minY = min(Ys)


minStemX = minY - 30*(minY/100)
minStemY = minY - 30*(minY/100)

maxStemX = maxX + 10*(maxX/100)
maxStemY = maxX + 10*(maxX/100)


	#print 'minX', minStemX, 'maxX', maxStemX
	#print 'minY', minStemY, 'maxY', maxStemY		
################

WindowController()
		