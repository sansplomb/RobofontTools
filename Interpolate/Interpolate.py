# -*- coding: utf8 -*-
from vanilla import *

af = AllFonts()
f = CurrentFont()


def createFontList():
	fontList = []
	for f in af:
		if f.info.familyName and f.info.styleName:
			if f.info.styleName == "Regular":
				fontList.append(f.info.familyName)
			else:
				fontList.append(f.info.familyName + " " + f.info.styleName)
		else:
			return
	return fontList
		
class InterpolateWindow(object):
	
	def __init__(self):
		self.selectedGlyphSet = ''
		selectedList = []
		for g in f:
			if g.selected:
				selectedList.append(g.name)
		selectedList.sort()
		for e in selectedList:
			self.selectedGlyphSet += e + ' '
	   
		self.fontSourceName = fontList[0]
		self.fontTargetName = fontList[0]
		self.fontSourceIndex = 0
		self.fontTargetIndex = 0
		self.interpolateXValue = 0
		self.interpolateYValue = 0
		self.scaleXValue = 100
		self.scaleYValue = 100
		self.keepStrokeXValue = 100
		self.keepStrokeYValue = 100
		self.currentFont = af[self.fontSourceIndex]
		self.selectedGlyphSetIndex = 0
		self.savedGlyphSets = {}
		for c_Font in af:
			if "GlyphSets" in c_Font.lib:
				for i in c_Font.lib["GlyphSets"]:
					self.savedGlyphSets[i] = c_Font.lib["GlyphSets"][i]
			else:
				#print "no saved glyph sets"
				#self.savedGlyphSets = {}
				c_Font.lib["GlyphSets"] = {}
			for glyphSet in self.savedGlyphSets.keys():
				c_Font.lib["GlyphSets"][glyphSet] = self.savedGlyphSets[glyphSet]
		
		if len(af[self.fontSourceIndex].info.postscriptStemSnapV) != 0:
			self.sourceRefX = af[self.fontSourceIndex].info.postscriptStemSnapV[0]
		else:
			self.sourceRefX = 0
		if len(af[self.fontSourceIndex].info.postscriptStemSnapH) != 0:
			self.sourceRefY = af[self.fontSourceIndex].info.postscriptStemSnapH[0]
		else:
			self.sourceRefY = 0
			
		if len(af[self.fontTargetIndex].info.postscriptStemSnapV) != 0:
			self.targetRefX = af[self.fontTargetIndex].info.postscriptStemSnapV[0]
		else:
			self.targetRefX = 0
		if len(af[self.fontTargetIndex].info.postscriptStemSnapH) != 0:
			self.targetRefY = af[self.fontTargetIndex].info.postscriptStemSnapH[0]
		else:
			self.targetRefY = 0
		
		self.sourceLayerList = af[self.fontSourceIndex].layerOrder
		self.targetLayerList = af[self.fontTargetIndex].layerOrder
		if len(self.sourceLayerList) > 0:
			self.sourceLayerName = self.sourceLayerList[0]
		else:
			self.sourceLayerName = "foreground"
		if len(self.targetLayerList) > 0:
			self.targetLayerName = self.targetLayerList[0]
		else:
			self.targetLayerName = "foreground"
		self.useSourceLayer = False
		self.useTargetLayer = False
		self.keepStrokeX = True
		self.keepStrokeY = True
		self.limitGlyphSet = False
		
		self.w = FloatingWindow((500, 600), "Interpolate")
		self.w.textBoxSource = TextBox((10, 10, 190, 20), "First Master")
		self.w.popUpButtonSource = PopUpButton((10, 30, 190, 20), fontList, callback=self.popUpButtonSourceCallback, sizeStyle = "regular")
		
		self.w.textBoxSourceLayer = TextBox((210, 10, 150, 20), "Layer")
		self.w.popUpButtonSourceLayer = PopUpButton((210, 30, 150, 20), self.sourceLayerList, callback=self.popUpButtonSourceLayerCallback, sizeStyle = "regular")
		self.w.textBoxSourceLayer.show(self.useSourceLayer)
		self.w.popUpButtonSourceLayer.show(self.useSourceLayer)
		
		self.w.textBoxSourceRefX = TextBox((370, 10, 50, 20), "Stem X")
		self.w.textBoxSourceRefY = TextBox((425, 10, 50, 20), "Stem Y")
		self.w.sourceRefXEditText = EditText((370, 30, 45, 20),
							callback=self.sourceRefXEditTextCallback)
		self.w.sourceRefYEditText = EditText((425, 30, 45, 20),
							callback=self.sourceRefYEditTextCallback)
		
		self.w.foregroundSourceCheckBox = CheckBox((10, 50, 150, 20), "Use Layer",
						   callback=self.foregroundSourceCheckBoxCallback, value=self.useSourceLayer)

		self.w.textBoxTarget = TextBox((10, 70, 190, 20), "Second Master")
		self.w.popUpButtonTarget = PopUpButton((10, 90, 190, 20), fontList, callback=self.popUpButtonTargetCallback, sizeStyle = "regular")
		
		self.w.textBoxTargetLayer = TextBox((210, 70, -10, 20), "Layer")
		self.w.popUpButtonTargetLayer = PopUpButton((210, 90, 150, 20), self.targetLayerList, callback=self.popUpButtonTargetLayerCallback, sizeStyle = "regular")
		self.w.textBoxTargetLayer.show(self.useTargetLayer)
		self.w.popUpButtonTargetLayer.show(self.useTargetLayer)
		
		self.w.textBoxTargetRefX = TextBox((370, 70, 50, 20), "Stem X")
		self.w.textBoxTargetRefY = TextBox((425, 70, 50, 20), "Stem Y")
		self.w.targetRefXEditText = EditText((370, 90, 45, 20),
							callback=self.targetRefXEditTextCallback)
		self.w.targetRefYEditText = EditText((425, 90, 45, 20),
							callback=self.targetRefYEditTextCallback)
		
		self.w.foregroundTargetCheckBox = CheckBox((10, 110, 150, 20), "Use Layer",
						   callback=self.foregroundTargetCheckBoxCallback, value=self.useTargetLayer)
		
		self.w.interpolateXTextBox = TextBox((10, 150, -10, 20), u"Interpolate X (‰)")
		self.w.interpolateXEditText = EditText((120, 150, 60, 20),
							callback=self.interpolateXEditTextCallback)
		self.w.resultingStemXTextBox = TextBox((190, 150, -10, 20), u"Result Stem X (FU)")
		self.w.resultingStemXEditText = EditText((310, 150, 60, 20),
							callback=self.resultingStemXEditTextCallback)
		self.w.interpolateXSlider = Slider((10, 180, -10, 23),
							tickMarkCount=7,
							value = 0,
							maxValue = 2000,
							minValue = -1000,
							callback=self.interpolateXSliderCallback)
							
		self.w.interpolateYTextBox = TextBox((10, 210, -10, 20), u"Interpolate Y (‰)")
		self.w.interpolateYEditText = EditText((120, 210, 60, 20),
							callback=self.interpolateYEditTextCallback)
		self.w.resultingStemYTextBox = TextBox((190, 210, -10, 20), u"Result Stem Y (FU)")
		self.w.resultingStemYEditText = EditText((310, 210, 60, 20),
							callback=self.resultingStemYEditTextCallback)
		self.w.interpolateYSlider = Slider((10, 240, -10, 23),
							tickMarkCount=7,
							value = 0,
							maxValue = 2000,
							minValue = -1000,
							callback=self.interpolateYSliderCallback)
							
		self.w.scaleXTextBox = TextBox((10, 290, -10, 20), "Scale X (%)")
		self.w.scaleXEditText = EditText((100, 290, 60, 20),
							callback=self.scaleXEditTextCallback)
		self.w.keepStrokeXCheckBox = CheckBox((170, 290, 200, 20), "keep stem (%)",
						   callback=self.keepStrokeXCheckBoxCallback, value=self.keepStrokeX)
		self.w.keepStrokeXEditText = EditText((280, 290, 40, 20),
							callback=self.keepStrokeXEditTextCallback)
		self.w.keepStrokeXSlider = Slider((330, 290, -10, 23),
							value = 100,
							maxValue = 100,
							minValue = 0,
							callback=self.keepStrokeXSliderCallback)				
		
		self.w.scaleXSlider = Slider((10, 320, -10, 23),
							tickMarkCount=5,
							value = 100,
							maxValue = 200,
							minValue = 1,
							callback=self.scaleXSliderCallback)
		
		self.w.scaleYTextBox = TextBox((10, 360, -10, 20), "Scale Y (%)")
		self.w.scaleYEditText = EditText((100, 360, 60, 20),
							callback=self.scaleYEditTextCallback)
		self.w.keepStrokeYCheckBox = CheckBox((170, 360, 200, 20), "keep stem (%)",
						   callback=self.keepStrokeYCheckBoxCallback, value=self.keepStrokeY)
		self.w.keepStrokeYEditText = EditText((280, 360, 40, 20),
							callback=self.keepStrokeYEditTextCallback)
		self.w.keepStrokeYSlider = Slider((330, 360, -10, 23),
							value = 100,
							maxValue = 100,
							minValue = 0,
							callback=self.keepStrokeYSliderCallback)
							
							
		self.w.scaleYSlider = Slider((10, 390, -10, 23),
							tickMarkCount=5,
							value = 100,
							maxValue = 200,
							minValue = 1,
							callback=self.scaleYSliderCallback)
							
		self.w.glyphSetCheckBox = CheckBox((10, 420, 200, 20), "Limit to Glyphs:",
								callback=self.glyphSetCheckBoxCallback, value=self.limitGlyphSet)
		self.w.popUpButtonGlyphSet = PopUpButton((210, 420, 180, 20), self.savedGlyphSets.keys(), callback=self.popUpButtonGlyphSetCallback, sizeStyle = "regular")
		self.w.buttonClearGlyphSet = Button((400, 420, -10, 20), "Clear Set",
							callback=self.buttonClearGlyphSetCallback)
		self.w.glyphSetTextEditor = TextEditor((10, 450, -10, 50),
							callback=self.glyphSetTextEditorCallback)
							
		self.w.glyphSetTextEditor.set(self.selectedGlyphSet)
		
		self.w.buttonSaveGlyphSet = Button((10, 510, 200, 20), "Save Glyph Set As",
							callback=self.buttonSaveGlyphSetCallback)
		self.w.saveGlyphSetEditText = EditText((220, 510, -10, 20),
							callback=self.saveGlyphSetEditTextCallback)
							
		self.w.bar = ProgressBar((10, -60, -10, 16), sizeStyle='small')
			
		self.fontSourceList = self.w.popUpButtonSource.getItems()
		self.fontTargetList = self.w.popUpButtonTarget.getItems()
		
		self.w.buttonOK = Button((10, -30, 90, -10), "Apply",
							callback=self.buttonOKCallback)
		self.w.buttonNew = Button((110, -30, 200, -10), "Apply in New Font",
							callback=self.buttonNewCallback)
		self.w.buttonCancel = Button((320, -30, -10, -10), "Close",
							callback=self.buttonCancelCallback)
		
		self.w.interpolateXEditText.set(self.interpolateXValue)
		self.w.interpolateYEditText.set(self.interpolateYValue)
		self.w.scaleXEditText.set(self.scaleXValue)
		self.w.scaleYEditText.set(self.scaleYValue)
	
		self.w.keepStrokeXEditText.set(self.keepStrokeXValue)
		self.w.keepStrokeYEditText.set(self.keepStrokeYValue)
		
		self.w.sourceRefXEditText.set(self.sourceRefX)
		self.w.sourceRefYEditText.set(self.sourceRefY)
		self.w.targetRefXEditText.set(self.targetRefX)
		self.w.targetRefYEditText.set(self.targetRefY)
		
		self.w.center()
		self.w.open()
		
	def resetAll(self):
		self.w.interpolateXEditText.set(0)
		self.w.interpolateYEditText.set(0)
		self.w.scaleXEditText.set(100)
		self.w.scaleYEditText.set(100)
		self.w.interpolateXSlider.set(0)
		self.w.interpolateYSlider.set(0)
		self.w.scaleXSlider.set(100)
		self.w.scaleYSlider.set(100)
		self.w.resultingStemXEditText.set(0)
		self.w.resultingStemYEditText.set(0)

		self.interpolateXValue = 0
		self.interpolateYValue = 0
		self.scaleXValue = 100
		self.scaleYValue = 100
		self.keepStrokeXValue = 100
		self.keepStrokeYValue = 100

	def calculateResultingStem(self, minStem, maxStem, value):
		if maxStem-minStem != 0:
			return int(value/(1000.0/(maxStem-minStem))+minStem)
		return 0

	def calculateInterpolatValueFromResultingStem(self, minStem, maxStem, result):
		if maxStem-minStem != 0:
			return int((result-minStem)*(1000.0/(maxStem-minStem)))
		return 0
		
	def keepStrokeXEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 0
			sender.set(0)
		self.keepStrokeXValue = newValue
		self.w.keepStrokeXSlider.set(newValue)
		self.setInterpolateX()
	
	def keepStrokeYEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 0
			sender.set(0)
		self.keepStrokeYValue = newValue
		self.w.keepStrokeYSlider.set(newValue)
		self.setInterpolateY()
		
	def keepStrokeXSliderCallback(self, sender):
		self.keepStrokeXValue = int(sender.get())
		self.w.keepStrokeXEditText.set(self.keepStrokeXValue)
		self.setInterpolateX()
	
	def keepStrokeYSliderCallback(self, sender):
		self.keepStrokeYValue = int(sender.get())
		self.w.keepStrokeYEditText.set(self.keepStrokeYValue)
		self.setInterpolateY()
		
	def buttonClearGlyphSetCallback(self, sender):
		if len(self.savedGlyphSets.keys()) > 0:
			#print self.selectedGlyphSetIndex
			#print self.savedGlyphSets.keys()
			currentsavedGlyphSet = self.savedGlyphSets.keys()[self.selectedGlyphSetIndex]
			for c_Font in af:
				#print 'delete', currentsavedGlyphSet
				if currentsavedGlyphSet in c_Font.lib["GlyphSets"]:
					del c_Font.lib["GlyphSets"][str(currentsavedGlyphSet)]
					self.savedGlyphSets = c_Font.lib["GlyphSets"]
					self.w.popUpButtonGlyphSet.setItems(self.savedGlyphSets.keys())
					self.w.glyphSetTextEditor.set('')
		self.selectedGlyphSetIndex = 0
	
	def popUpButtonGlyphSetCallback(self, sender):
		self.selectedGlyphSetIndex = sender.get()
		self.currentFont = af[self.fontSourceIndex]
		savedglyphSetsList = self.savedGlyphSets.keys()
		#print savedglyphSetsList[sender.get()]
		content =  self.savedGlyphSets[savedglyphSetsList[sender.get()]]
		#print content
		self.w.glyphSetTextEditor.set(str(content))
		self.selectedGlyphSetIndex
		self.selectedGlyphSet = str(content)
		
	def buttonSaveGlyphSetCallback(self, sender):
		self.currentFont = af[self.fontSourceIndex]
		newGlyphSetName = self.w.saveGlyphSetEditText.get()
		newGlyphSet = self.selectedGlyphSet
		for c_Font in af:
			if newGlyphSetName != '' and newGlyphSet != '': 
				c_Font.lib["GlyphSets"][newGlyphSetName] = newGlyphSet
				self.savedGlyphSets[newGlyphSetName] = newGlyphSet
				savedglyphSetsList = self.savedGlyphSets.keys()
				self.w.popUpButtonGlyphSet.setItems(savedglyphSetsList)
		
	
	def saveGlyphSetEditTextCallback(self, sender):
		self.w.saveGlyphSetEditText.set(sender.get())
	
	def glyphSetTextEditorCallback(self, sender):
		self.selectedGlyphSet = sender.get()
		self.w.glyphSetCheckBox.set(True)
		self.limitGlyphSet = True
	
	def glyphSetCheckBoxCallback(self, sender):
		self.limitGlyphSet = sender.get()
	
	def keepStrokeXCheckBoxCallback(self, sender):
		self.keepStrokeX = sender.get()
		if self.keepStrokeX:
			self.setInterpolateX()
	
	def keepStrokeYCheckBoxCallback(self, sender):
		self.keepStrokeY = sender.get()
		if self.keepStrokeY:
			self.setInterpolateY()
		
	def foregroundSourceCheckBoxCallback(self, sender):
		self.w.popUpButtonSourceLayer.show(sender.get())
		self.w.textBoxSourceLayer.show(sender.get())
		self.useSourceLayer = sender.get()
		
	def foregroundTargetCheckBoxCallback(self, sender):
		self.w.popUpButtonTargetLayer.show(sender.get())
		self.w.textBoxTargetLayer.show(sender.get())
		self.useTargetLayer = sender.get()
		
	def interpolateXSliderCallback(self, sender):
		#print "slider edit!", sender.get()
		self.interpolateXValue = int(sender.get())
		self.w.interpolateXEditText.set(self.interpolateXValue)
		stemX = self.calculateResultingStem(self.sourceRefX, self.targetRefX, self.interpolateXValue)
		self.w.resultingStemXEditText.set(stemX)
	
	def interpolateYSliderCallback(self, sender):
		self.interpolateYValue = int(sender.get())
		self.w.interpolateYEditText.set(self.interpolateYValue)
		stemY = self.calculateResultingStem(self.sourceRefY, self.targetRefY, self.interpolateYValue)
		self.w.resultingStemYEditText.set(stemY)
	
	def setInterpolateX(self):
		if self.keepStrokeX:
			if self.sourceRefX != self.targetRefX:
				interpolXValue = (self.keepStrokeXValue/100) * (1000*(self.sourceRefX *(100-self.scaleXValue)) / ((self.targetRefX - self.sourceRefX) * self.scaleXValue))
			else:
				interpolXValue = 0
			self.interpolateXValue = int(interpolXValue)
			self.w.interpolateXEditText.set(self.interpolateXValue)
			self.w.interpolateXSlider.set(self.interpolateXValue)
			
	def setInterpolateY(self):
		if self.keepStrokeY:
			if self.sourceRefY != self.targetRefY:
				interpolYValue = (self.keepStrokeYValue/100) * (1000*(self.sourceRefY *(100-self.scaleYValue)) / ((self.targetRefY - self.sourceRefY) * self.scaleYValue))
			else:
				interpolYValue = 0
			self.interpolateYValue = int(interpolYValue)
			self.w.interpolateYEditText.set(self.interpolateYValue)
			self.w.interpolateYSlider.set(self.interpolateYValue)
		
	def scaleXSliderCallback(self, sender):
		self.scaleXValue = float(sender.get())
		self.w.scaleXEditText.set(self.scaleXValue)
		self.setInterpolateX()
		
	
	def scaleYSliderCallback(self, sender):
		self.scaleYValue = float(sender.get())
		self.w.scaleYEditText.set(self.scaleYValue)
		self.setInterpolateY()
	
		
	def popUpButtonSourceCallback(self, sender):		
		self.resetAll()
		self.fontSourceIndex = sender.get()
		self.fontSourceName = self.fontSourceList[sender.get()]
		self.w.popUpButtonSourceLayer.setItems(af[self.fontSourceIndex].layerOrder)
		self.sourceLayerList = af[self.fontSourceIndex].layerOrder
		if len(self.sourceLayerList) > 0:
			self.sourceLayerName = self.sourceLayerList[0]
		else:
			self.sourceLayerName = "foreground"
		if len(af[self.fontSourceIndex].info.postscriptStemSnapV) != 0:
			self.sourceRefX = af[self.fontSourceIndex].info.postscriptStemSnapV[0]
		else:
			self.sourceRefX = 0
		self.w.sourceRefXEditText.set(self.sourceRefX)
		if len(af[self.fontSourceIndex].info.postscriptStemSnapH) != 0:
			self.sourceRefY = af[self.fontSourceIndex].info.postscriptStemSnapH[0]
		else:
			self.sourceRefY = 0
		self.w.sourceRefYEditText.set(self.sourceRefY)
		
	def popUpButtonTargetCallback(self, sender):
		self.resetAll()		
		self.fontTargetIndex = sender.get()
		self.fontTargetName = self.fontTargetList[sender.get()]
		self.w.popUpButtonTargetLayer.setItems(af[self.fontTargetIndex].layerOrder)
		self.targetLayerList = af[self.fontTargetIndex].layerOrder
		if len(self.targetLayerList) > 0:
			self.targetLayerName = self.targetLayerList[0]
		else:
			self.targetLayerName = "foreground"
		if len(af[self.fontTargetIndex].info.postscriptStemSnapV) != 0:
			self.targetRefX = af[self.fontTargetIndex].info.postscriptStemSnapV[0]
		else:
			self.targetRefX = 0
		self.w.targetRefXEditText.set(self.targetRefX)
		if len(af[self.fontTargetIndex].info.postscriptStemSnapH) != 0:
			self.targetRefY = af[self.fontTargetIndex].info.postscriptStemSnapH[0]
		else:
			self.targetRefY = 0
		self.w.targetRefYEditText.set(self.targetRefY)

		
	def popUpButtonSourceLayerCallback(self, sender):
		self.sourceLayerIndex = sender.get()
		self.sourceLayerName = self.sourceLayerList[self.sourceLayerIndex]
		
	def popUpButtonTargetLayerCallback(self, sender):
		self.targetLayerIndex = sender.get()
		self.targetLayerName = self.targetLayerList[self.targetLayerIndex]
	
	def isInteger(self, string):
		try:
			return int(string)
		except ValueError:
			return 0
			
	def sourceRefXEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 0
			sender.set(0)
		self.sourceRefX = newValue
		
	def sourceRefYEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 0
			sender.set(0)
		self.sourceRefY = newValue
		
	def targetRefXEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 0
			sender.set(0)
		self.targetRefX = newValue
		
	def targetRefYEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 0
			sender.set(0)
		self.targetRefY = newValue
	
	def interpolateXEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			if sender.get() == '-':
				newValue = 0
			else:
				newValue = 0
				sender.set(0)
		self.w.interpolateXSlider.set(newValue)
		self.interpolateXValue = newValue
		stemX = self.calculateResultingStem(self.sourceRefX, self.targetRefX, self.interpolateXValue)
		self.w.resultingStemXEditText.set(stemX)
		
	def interpolateYEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			if sender.get() == '-':
				newValue = 0
			else:
				newValue = 0
				sender.set(0)
		self.w.interpolateYSlider.set(newValue)
		self.interpolateYValue = newValue
		stemY = self.calculateResultingStem(self.sourceRefY, self.targetRefY, self.interpolateYValue)
		self.w.resultingStemYEditText.set(stemY)

	def resultingStemXEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 0
			sender.set(0)

		interpolValue = self.calculateInterpolatValueFromResultingStem(self.sourceRefX, self.targetRefX, newValue)
		self.w.interpolateXEditText.set(interpolValue)
		self.w.interpolateXSlider.set(interpolValue)
		self.interpolateXValue = interpolValue

	def resultingStemYEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 0
			sender.set(0)

		interpolValue = self.calculateInterpolatValueFromResultingStem(self.sourceRefY, self.targetRefY, newValue)
		self.w.interpolateYEditText.set(interpolValue)
		self.w.interpolateYSlider.set(interpolValue)
		self.interpolateYValue = interpolValue
		
	def scaleXEditTextCallback(self, sender):
		try:
			newValue = float(sender.get())
		except ValueError:
			newValue = 1
			sender.set(1)
		if newValue == 0:
			newValue = 1
			sender.set(1)
		self.w.scaleXSlider.set(newValue)
		self.scaleXValue = newValue
		self.setInterpolateX()
		
	def scaleYEditTextCallback(self, sender):
		try:
			newValue = float(sender.get())
		except ValueError:
			newValue = 1
			sender.set(1)
		if newValue == 0:
			newValue = 1
			sender.set(1)
		self.w.scaleYSlider.set(newValue)
		self.scaleYValue = newValue
		self.setInterpolateY()
		
	def findMatchingIndexes(self, componentName, gS, gT):
		for iS in range(len(gS.components)):
			for iT in range(len(gT.components)):
				if componentName == gS.components[iS].baseGlyph == gT.components[iT].baseGlyph:
					return (iS, iT)
	
	def interpol(self, gS, gT, valueX, valueY):
		gI = gS.copy()
		for i in range(len(gS)):
			for j in range(len(gS[i].points)):
				sourcePoint = self.allSourcePoints[i][j]
				targetPoint = self.allTargetPoints[i][j]
				gI[i].points[j].x = int((sourcePoint[0] + ((targetPoint[0] - sourcePoint[0]) * valueX/1000)) * self.scaleXValue/100)
				gI[i].points[j].y = int((sourcePoint[1] + ((targetPoint[1] - sourcePoint[1]) * valueY/1000)) * self.scaleYValue/100)
		if gI.components > 0:
			for i in range(len(gI.components)):
				if gS.components[i].baseGlyph == gT.components[i].baseGlyph:
					indexS = i
					indexT = i
				else:
					(indexS, indexT) = self.findMatchingIndexes(gI.components[i].baseGlyph, gS, gT)
					
				if indexS != None and indexT != None:
					gI.components[i].offset = ( int( (gS.components[indexS].offset[0] + ((gT.components[indexT].offset[0] - gS.components[indexS].offset[0]) * valueX/1000)) * self.scaleXValue/100 ), int( (gS.components[indexS].offset[1] + ((gT.components[indexT].offset[1] - gS.components[indexS].offset[1]) * valueX/1000)) * self.scaleXValue/100 ) )
				else:
					print 'ERROR: components not matching'
		gI.width = int((gS.width + ((gT.width - gS.width) * valueX/1000)) * self.scaleXValue/100)
		return gI
			
	def collaPolate(self, gS, gT, barIncrement):
		self.w.bar.increment(barIncrement)
		#Collect Master1 points
		self.allSourcePoints = []
		self.allSourcePointsLength = []
		if self.useSourceLayer:
			sourceLayer = gS.getLayer(self.sourceLayerName)
		else:
			sourceLayer = gS
	
		for i in range(len(sourceLayer)):
			self.allSourcePoints.append([])
			for j in range(len(sourceLayer[i].points)):
				
				self.allSourcePoints[i].append((sourceLayer[i].points[j].x, sourceLayer[i].points[j].y))
				self.allSourcePointsLength.append(j)
								
		#Collect Master2 points
		self.allTargetPoints = []
		self.allTargetPointsLength = []
		if self.useTargetLayer:
			targetLayer = gT.getLayer(self.targetLayerName)
		else:
			targetLayer = gT
		
		for i in range(len(targetLayer)):
			self.allTargetPoints.append([])
			for j in range(len(targetLayer[i].points)):
				
				self.allTargetPoints[i].append((targetLayer[i].points[j].x, targetLayer[i].points[j].y))
				self.allTargetPointsLength.append(j)
		##
		
		if self.allSourcePointsLength != self.allTargetPointsLength:
			print 'Warning: Glyph ' + gS.name + ' masters not matching'
			gS.mark = (1, 0, 0, 0.5)
			#print self.allSourcePoints
			#print self.allTargetPoints
		else:
			gI = self.interpol(gS, gT, self.interpolateXValue, self.interpolateYValue)	
			if self.new:
				self.newFont.newGlyph(gI.name)
				self.newFont[gI.name] = gI
				#self.newFont[gI.name].update()
			else:
				self.sourceFont[gI.name] = gI
				#self.sourceFont[gI.name].update()
							
	def buttonOKCallback(self, sender):
		self.new = False
		self.w.bar.set(0)
		self.sourceFont = af[self.fontSourceIndex]
		self.targetFont = af[self.fontTargetIndex]
		barIncrement = 100/len(self.targetFont)
		for gT in self.targetFont:
			self.w.bar.increment(barIncrement)
			for gS in self.sourceFont:
				if gT.name == gS.name:
					if self.limitGlyphSet:
						s = str(self.selectedGlyphSet)
						l = s.split(' ')
						if gT.name in l:
							self.collaPolate(gS, gT, barIncrement)
					else:
						self.collaPolate(gS, gT, barIncrement)
		self.sourceFont.update()
		self.w.bar.set(0)

		#self.w.close()
		
	def buttonNewCallback(self, sender):
		self.new = True
		self.newFont = RFont()
		if len(self.newFont) != 0:
			barIncrement = 100/len(self.newFont)
		else:
			barIncrement = 100
		for g in self.newFont:
			if g:
				self.newFont.removeGlyph(g.name)
				self.w.bar.increment(barIncrement)
		self.w.bar.set(0)
		self.sourceFont = af[self.fontSourceIndex]
		self.targetFont = af[self.fontTargetIndex]
		
		barIncrement = 100/len(self.targetFont)
		for gT in self.targetFont:
			for gS in self.sourceFont:
				if gT.name == gS.name:
					if self.limitGlyphSet:
						s = str(self.selectedGlyphSet)
						l = s.split(' ')
						if gT.name in l:
							self.collaPolate(gS, gT, barIncrement)
					else:
						self.collaPolate(gS, gT, barIncrement)
		self.newFont.update()
		
		master1_kerning = self.sourceFont.kerning
		master2_kerning = self.targetFont.kerning
		kerning1Items = master1_kerning.items()
		kerning2Items = master2_kerning.items()
		groups1Items = self.sourceFont.groups.items()
		groups2Items = self.targetFont.groups.items()
		
		for (groupName1, grouppedGlyphs1) in groups1Items:
			for (groupName2, grouppedGlyphs2) in groups2Items:
				grouppedGlyphs1.sort()
				grouppedGlyphs2.sort()
				if groupName1 == groupName2 and grouppedGlyphs1 == grouppedGlyphs2:
					self.newFont.groups[groupName1] = grouppedGlyphs1
		
		newKerning = {}
		for (pair1, value1) in kerning1Items:
			#for (pair2, value2) in kerning2Items:
			if pair1 in master2_kerning:
				value2 = master2_kerning[pair1]
				interpolatedValue = int((value1 + ((value2 - value1) * self.interpolateXValue/1000.0)) * self.scaleXValue/100.0)
				#self.newFont.kerning[pair1] = interpolatedValue
				newKerning[pair1] = interpolatedValue
			else:
				interpolatedValue = int((value1 * self.interpolateXValue/1000.0) * self.scaleXValue/100.0)
				newKerning[pair1] = interpolatedValue
		for (pair2, value2) in kerning2Items:
			if pair2 not in master1_kerning:
				interpolatedValue = int( (value2 * self.interpolateXValue/1000.0) * self.scaleXValue/100.0)
				newKerning[pair2] = interpolatedValue

		self.newFont.kerning.update(newKerning)

		dictinfo = self.newFont.info.asDict()

		for elem in sorted(dictinfo.keys()):
			self.newFont.info.__setattr__(elem, self.sourceFont.info.__getattr__(elem))
			if self.sourceFont.info.__getattr__(elem) != None:
				#print(str(elem) + " = " + str(self.sourceFont.info.__getattr__(elem)))
				if str(elem) in ["ascender", "capHeight", "descender", "xHeight", "openTypeHheaAscender", "openTypeHheaDescender", "openTypeHheaLineGap", "openTypeOS2TypoAscender", "openTypeOS2TypoDescender", "openTypeOS2TypoLineGap", "openTypeOS2WinAscent", "openTypeOS2WinDescent", ""]:
					source = self.sourceFont.info.__getattr__(elem)
					target = self.targetFont.info.__getattr__(elem)
					interpolated = int((source + ((target - source) * self.interpolateYValue/1000.0)) * self.scaleYValue/100.0)
					print str(elem), ': ', source, target, '-->', interpolated
					self.newFont.info.__setattr__(elem, interpolated)
				if str(elem) in ["postscriptBlueValues", "postscriptOtherBlues", "postscriptStemSnapH", "postscriptStemSnapV"]:
					source = self.sourceFont.info.__getattr__(elem)
					target = self.targetFont.info.__getattr__(elem)
					interpolatedList = []
					if len(source) == len(target):
						for i in range(len(source)):
							interpolated = int((source[i] + ((target[i] - source[i]) * self.interpolateYValue/1000.0)) * self.scaleYValue/100.0)
							interpolatedList.append(interpolated)
					print str(elem), ': ', source, target, '-->', interpolatedList
					self.newFont.info.__setattr__(elem, interpolatedList)

			
		self.w.bar.set(0)
		 
	def buttonCancelCallback(self, sender):
		 #print "Cancel"
		 self.w.close()


fontList = createFontList()
if fontList:
	InterpolateWindow()
else:
	print 'All open fonts must have familyName and styleName'
