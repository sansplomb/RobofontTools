from vanilla import *
import string, sys


af = AllFonts()
f = CurrentFont()


def createFontList():
	fontList = []
	for f in af:
		if f.info.familyName and f.info.styleName:
			fontList.append(f.info.familyName + " " + f.info.styleName)
		else:
			return
	return fontList
		
class AssignFontLayerWindow(object):
	
	def __init__(self):
		self.w = Window((200, 300), "Assign Font Layer")
		self.w.textBoxSource = TextBox((10, 10, -10, 30), "Source Font:")
		self.w.popUpButtonSource = PopUpButton((10, 30, -10, 30), fontList, callback=self.popUpButtonSourceCallback, sizeStyle = "regular")
		
		self.w.textBoxTarget = TextBox((10, 70, -10, 30), "Target Font:")
		self.w.popUpButtonTarget = PopUpButton((10, 90, -10, 30), fontList, callback=self.popUpButtonTargetCallback, sizeStyle = "regular")
		
		self.w.textBox = TextBox((10, 130, -10, 30), "Layer Name in Target Font:")
		self.w.editText = EditText((10, 160, -10, 30),
							callback=self.editTextCallback)
	
		self.fontSourceName = fontList[0]
		self.fontTargetName = fontList[0]
		self.fontSourceIndex = 0
		self.fontTargetIndex = 0
		
		self.fontSourceList = self.w.popUpButtonSource.getItems()
		self.fontTargetList = self.w.popUpButtonTarget.getItems()
		
		self.w.buttonOK = Button((10, -30, 90, -10), "OK",
							callback=self.buttonOKCallback)
		self.w.buttonCancel = Button((110, -30, -10, -10), "Cancel",
							callback=self.buttonCancelCallback)
		self.layerName = "untitled_layer"
		self.w.editText.set(self.layerName)
		self.w.center()
		self.w.open()
		
	def buttonOKCallback(self, sender):
		 #print "Ok"
		 
		sourceFont = af[self.fontSourceIndex]
		targetFont = af[self.fontTargetIndex]
		#print "Source Font:", sourceFont
		#print "Target Font:", targetFont
		#print "New Layer Name:", self.layerName
		 
		 #get the first glyph's name
		firstGlyphName = targetFont.keys()[0]
		 #create a new layer with specified layerName
		targetFont[firstGlyphName].getLayer(self.layerName)
		 #parse the target font's glyphs
		for gT in targetFont:
		 	#parse the source font's glyphs
			for gS in sourceFont:
		 		#if their names match, I want the targetLayer to be a copy of the sourceLayer
				if gT.name == gS.name:
					sourceLayer = gS.getLayer("foreground")
		 			targetLayer = gT.getLayer(self.layerName)
		 			#clear contours if any
		 			targetLayer.clear()
		 			targetWidth = gT.width
		 			gT.flipLayers("foreground", self.layerName)
					targetFont[gT.name] = gS.copy()
					targetFont[gT.name].width = targetWidth
					gT.flipLayers("foreground", self.layerName)
		self.w.close()
		 
	def buttonCancelCallback(self, sender):
		 #print "Cancel"
		 self.w.close()
		
	def popUpButtonSourceCallback(self, sender):
		#print "pop up button selection!", sender.get()
		
		self.fontSourceIndex = sender.get()
		self.fontSourceName = self.fontSourceList[sender.get()]
		#print self.fontName
		
	def popUpButtonTargetCallback(self, sender):
		#print "pop up button selection!", sender.get()
		
		self.fontTargetIndex = sender.get()
		self.fontTargetName = self.fontTargetList[sender.get()]
		#print self.fontName
		
	def editTextCallback(self, sender):

		#layerName = sender.get().title()
		layerName = ''
		layerNameList = sender.get().split(" ")
		for i in range(len(layerNameList)):
			layerName += layerNameList[i]
			if i < len(layerNameList)-1:
				layerName += '_'
		self.layerName = layerName

fontList = createFontList()
if fontList:
	AssignFontLayerWindow()
else:
	print 'All open fonts must have familyName and styleName'