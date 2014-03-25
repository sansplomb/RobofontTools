from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController
import math 

inferiors = {
	'zeroinferior': ['zerosuperior'],
	'oneinferior': ['onesuperior'],
	'twoinferior': ['twosuperior'],
	'threeinferior': ['threesuperior'],
	'fourinferior': ['foursuperior'],
	'fiveinferior': ['fivesuperior'],
	'sixinferior': ['sixsuperior'],
	'seveninferior': ['sevensuperior'],
	'eightinferior': ['eightsuperior'],
	'nineinferior': ['ninesuperior']
	}
	
numerators = {
	'zero.numerator': ['zerosuperior'],
	'one.numerator': ['onesuperior'],
	'two.numerator': ['twosuperior'],
	'three.numerator': ['threesuperior'],
	'four.numerator': ['foursuperior'],
	'five.numerator': ['fivesuperior'],
	'six.numerator': ['sixsuperior'],
	'seven.numerator': ['sevensuperior'],
	'eight.numerator': ['eightsuperior'],
	'nine.numerator': ['ninesuperior']
	}

denominators = {
	'zero.denominator': ['zerosuperior'],
	'one.denominator': ['onesuperior'],
	'two.denominator': ['twosuperior'],
	'three.denominator': ['threesuperior'],
	'four.denominator': ['foursuperior'],
	'five.denominator': ['fivesuperior'],
	'six.denominator': ['sixsuperior'],
	'seven.denominator': ['sevensuperior'],
	'eight.denominator': ['eightsuperior'],
	'nine.denominator': ['ninesuperior']
	}

fractionsML = {
	'onehalf': ['onesuperior', 'fraction', 'twosuperior'],
	'onequarter': ['onesuperior', 'fraction', 'foursuperior'],
	'threequarters': ['threesuperior', 'fraction', 'foursuperior'],
	'onethird': ['onesuperior', 'fraction', 'threesuperior'],
	'twothirds': ['twosuperior', 'fraction', 'threesuperior'],
	'oneeighth': ['onesuperior', 'fraction', 'eightsuperior'],
	'threeeighths': ['threesuperior', 'fraction', 'eightsuperior'],
	'fiveeighths': ['fivesuperior', 'fraction', 'eightsuperior'],
	'seveneighths': ['sevensuperior', 'fraction', 'eightsuperior'],
	'onefifth': ['onesuperior', 'fraction', 'fivesuperior'],
	'twofifths': ['twosuperior', 'fraction', 'fivesuperior'],
	'threefifths': ['threesuperior', 'fraction', 'fivesuperior'],
	'fourfifths': ['foursuperior', 'fraction', 'fivesuperior'],
	'onesixth': ['onesuperior', 'fraction', 'sixsuperior'],
	'fivesixths': ['fivesuperior', 'fraction', 'sixsuperior'],
	'oneseventh': ['onesuperior', 'fraction', 'sevensuperior'],
	'twosevenths': ['twosuperior', 'fraction', 'sevensuperior'],
	'threesevenths': ['threesuperior', 'fraction', 'sevensuperior'],
	'foursevenths': ['foursuperior', 'fraction', 'sevensuperior'],
	'fivesevenths': ['fivesuperior', 'fraction', 'sevensuperior'],
	'sixsevenths': ['sixsuperior', 'fraction', 'sevensuperior'],
	'oneninth': ['onesuperior', 'fraction', 'ninesuperior'],
	'twoninths': ['twosuperior', 'fraction', 'ninesuperior'],
	'fourninths': ['foursuperior', 'fraction', 'ninesuperior'],
	'fiveninths': ['fivesuperior', 'fraction', 'ninesuperior'],
	'sevenninths': ['sevensuperior', 'fraction', 'ninesuperior'],
	'eightninths': ['eightsuperior', 'fraction', 'ninesuperior']
	}

fractionsS = {
	'onehalf': ['onesuperior', 'fraction', 'twosuperior'],
	'onequarter': ['onesuperior', 'fraction', 'foursuperior'],
	'threequarters': ['threesuperior', 'fraction', 'foursuperior'],
	}
	
class Process(BaseWindowController):

	def __init__(self):
		self.w = FloatingWindow((310, 150))
		
		self.w.textBox = TextBox((10, 10, -10, 16), "Fractions & Ordinals", sizeStyle = "regular", alignment = "center")
		self.w.textBoxEncodingS = CheckBox((10, 40, -10, 20), "Encoding S", sizeStyle = "small", 
											callback=self.textBoxEncodingSCallback, value = False)
		self.w.textBoxEncodingML = CheckBox((10, 70, -10, 20), "Encoding M & L", sizeStyle = "small", 
											callback=self.textBoxEncodingMLCallback, value = False)

		self.w.buttonMake = Button((10, -20, 90, 15), "Make", sizeStyle = "small", callback=self.showProgress)
		self.w.buttonDelete = Button((110, -20, 90, 15), "Delete All", sizeStyle = "small", callback=self.showDelete)
		self.w.buttonClose = Button((210, -20, 90, 15), "Close", sizeStyle = "small", callback=self.closeWindow)
		
		self.w.center()
		self.w.open()
		
	def closeWindow(self, sender):
		self.w.close()
		
	def textBoxEncodingSCallback(self, sender):
		if sender.get():
			self.w.textBoxEncodingML.set(False)
		
	def textBoxEncodingMLCallback(self, sender):
		if sender.get():
			self.w.textBoxEncodingS.set(False)
	
	def showProgress(self, sender):
		if self.w.textBoxEncodingML.get():
			self.progress = self.startProgress("Checking UFO...", tickCount=100)
			fractionsToMake = self.defineGlyphsToMake(f, fractionsML)
			self.progress.close()
			self.progress = self.startProgress("Making Fractions M & L...", tickCount=100)
			self.makeFractions(fractionsToMake)
			self.progress.close()
		
			self.progress = self.startProgress("Checking UFO...", tickCount=100)
			inferiorsToMake = self.defineGlyphsToMake(f, inferiors)
			self.progress.close()
			self.progress = self.startProgress("Making Inferiors...", tickCount=100)
			self.makeInferiors(inferiorsToMake)
			self.progress.close()
		
			self.progress = self.startProgress("Checking UFO...", tickCount=100)
			numeratorsToMake = self.defineGlyphsToMake(f, numerators)
			self.progress.close()
			self.progress = self.startProgress("Making Numerators...", tickCount=100)
			self.makeNumerators(numeratorsToMake)
			self.progress.close()

			self.progress = self.startProgress("Checking UFO...", tickCount=100)
			denominatorsToMake = self.defineGlyphsToMake(f, denominators)
			self.progress.close()
			self.progress = self.startProgress("Making Denominators...", tickCount=100)
			self.makeDenominators(denominatorsToMake)
			self.progress.close()
			
		elif self.w.textBoxEncodingS.get:
			self.progress = self.startProgress("Checking UFO...", tickCount=100)
			fractionsToMake = self.defineGlyphsToMake(f, fractionsS)
			self.progress.close()
			self.progress = self.startProgress("Making Fractions S...", tickCount=100)
			self.makeFractions(fractionsToMake)
			self.progress.close()
		
		self.w.close()
	
	def showDelete(self, sender):
		self.progress = self.startProgress("Deleting...", tickCount=100)
		self.deleteAll(f)
		self.progress.close()
		
	def deleteAll(self, f):
		self.progress.setTickCount(len(fractionsML.keys()) + len(inferiors.keys()) + len(numerators.keys()) + len(denominators.keys()))
		for i in fractionsML.keys():
			self.progress.update()
			if i in f.keys():
				f.removeGlyph(i)
		for i in inferiors.keys():
			self.progress.update()
			if i in f.keys():
				f.removeGlyph(i)
		for i in numerators.keys():
			self.progress.update()
			if i in f.keys():
				f.removeGlyph(i)
		for i in denominators.keys():
			self.progress.update()
			if i in f.keys():
				f.removeGlyph(i)
				
	def defineGlyphsToMake(self, f, glyphsDict):
		glyphsToMake = {}
		self.progress.setTickCount(len(glyphsDict.keys()))
		for i in glyphsDict.keys():
			self.progress.update()
			newGlyphName = i
			if i in f.keys():
				#print 'glyph ' + i + ' already exists'
				continue
			else:
				componentsList = []
				for j in glyphsDict[i]:
					missing = False
					if j in f.keys():
						#print 'glyph ' + j + ' in the font'
						componentsList.append(j)
						continue
					else:
						missing = True
				if missing == False:
					glyphsToMake[i] = componentsList
	
		return glyphsToMake

	def makeFractions(self, fractionsDict):
		self.progress.setTickCount(len(fractionsDict.keys()))
		for i in fractionsDict.keys():
			self.progress.update()
			f.newGlyph(i)
			f[i].mark = (1, 0, 1, 0.5)
			firstSup = fractionsDict[i][0] 
			fraction = fractionsDict[i][1]
			secondInf = fractionsDict[i][2] 
			f[i].width = f[firstSup].width + f[fraction].width + f[secondInf].width
			f[i].appendComponent(firstSup, (0, 0))
			f[i].appendComponent(fraction, (f[firstSup].width, 0))
			f[i].appendComponent(secondInf, (f[firstSup].width + f[fraction].width + xShiftInferiors, yShiftInferiors))

	def makeInferiors(self, inferiorsDict):
		self.progress.setTickCount(len(inferiorsDict.keys()))
		for i in inferiorsDict.keys():
			self.progress.update()
			f.newGlyph(i)
			f[i].mark = (1, 0, 0, 0.5)
			component = inferiorsDict[i][0]
			f[i].width = f[component].width
			f[i].appendComponent(component, (xShiftInferiors, yShiftInferiors))

	def makeNumerators(self, numeratorsDict):
		self.progress.setTickCount(len(numeratorsDict.keys()))
		for i in numeratorsDict.keys():
			self.progress.update()
			f.newGlyph(i)
			f[i].mark = (1, 0, 0, 0.5)
			component = numeratorsDict[i][0]
			f[i].width = f[component].width
			f[i].appendComponent(component, (xShiftNumerators, yShiftNumerators))
		
	def makeDenominators(self, denominatorsDict):
		self.progress.setTickCount(len(denominatorsDict.keys()))
		for i in denominatorsDict.keys():
			self.progress.update()
			f.newGlyph(i)
			f[i].mark = (1, 0, 0, 0.5)
			component = denominatorsDict[i][0]
			f[i].width = f[component].width
			f[i].appendComponent(component, (xShiftDenominators, yShiftDenominators))

def getItalAngle(f):
	italAngle = f.info.italicAngle
	if italAngle == None:
		italAngle = 0
	return italAngle

def getItalRatio(italAngle):
	italRatio = math.tan(math.radians(-italAngle))
	return italRatio

def getxShift(yShift, italRatio):
	xShift = int(yShift * italRatio)
	return xShift



f = CurrentFont()
italAngle = getItalAngle(f)
italRatio = getItalRatio(italAngle)

zeroSupHeight = f['zerosuperior'].box[3] - f['zerosuperior'].box[1]

yShiftInferiors = - f['onesuperior'].box[1]
xShiftInferiors = getxShift(yShiftInferiors, italRatio)

yShiftNumerators = zeroSupHeight * 30/100
xShiftNumerators = getxShift(yShiftNumerators, italRatio)

yShiftDenominators = - f['onesuperior'].box[1] - zeroSupHeight * 30/100
xShiftDenominators = getxShift(yShiftDenominators, italRatio)

Process()
f.update()
