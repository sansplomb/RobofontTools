#coding=utf-8
from lib.fontObjects.doodleFontCompiler.ttfCompiler import TTFCompilerSettings
from lib.doodleMenus import BaseMenu
from mojo.events import *
from mojo.extensions import *
from mojo.UI import *
from AppKit import *
from vanilla import *
from ctypes import *
import freetype
import os, math

#from proxy import MenuProxy

def difference(point1, point2):
	return ((point1.x - point2.x), (point1.y - point2.y))

def pointsApproxEqual(p_glyph, p_cursor):
	return (abs(p_glyph.x - p_cursor[0]) < 10) and (abs(p_glyph.y - p_cursor[1]) < 10)

def find_in_list(l, p):
	for e in l:
		if p(e):
			return e
	return None

def getAngle((x1, y1), (x2, y2)):
	xDiff = x2-x1
	yDiff= y2-y1 
	return math.atan2(yDiff,xDiff)

toolbarIcon = ExtensionBundle("TTH").get("toolbarIcon")

class hintTT(object):
	def __init__(self, axis, instructionType, inPointIndex, outPointIndex, controlValue):
		self.axis = axis
		self.instructionType = instructionType
		self.inPointIndex = inPointIndex
		self.outPointIndex = outPointIndex
		self.controlValue = controlValue
		sharedInstance = self

class TTH_Set(object):
	def __init__(self, axis, set_type, instructions):
		self.axis = axis
		self.set_type = set_type
		self.instructions = instructions


class CallBackCVT():
	def __init__(self, controlValue, TTHtoolInstance):
		self.index = controlValue[0]
		self.name = controlValue[1]
		self.value = controlValue[2]
		self.TTHtoolInstance = TTHtoolInstance

	def __call__(self, controlValue):
		#print self.index, self.name, self.value
		controlValueIndex = self.index
		self.TTHtoolInstance.set_currentControlValue(controlValueIndex)
		self.TTHtoolInstance.set_currentTool('Link_CVT')

class TTHTool(BaseEventTool):

	def __init__(self):
		BaseEventTool.__init__(self)
		self.g = CurrentGlyph()
		self.undoStorage = {}
		self.redoStorage = {}

	##############

	def set_currentControlValue(self, controlValueIndex):
		self.controlValueIndex = controlValueIndex

	def set_currentTool(self, currentTool):
		self.currentTool = currentTool
	##############

	### TTH Tool Icon ###
	def getToolbarIcon(self):
		## return the toolbar icon
		return toolbarIcon
		
	def getToolbarTip(self):
		return "TTH Hinting Tool"
	###############

	### TTH freetype ###
	def generateTempFont(self):
		tempFont = RFont(showUI=False)
		tempGlyph = self.g.copy()

		tempFont.info.unitsPerEm = CurrentFont().info.unitsPerEm
		tempFont.info.ascender = CurrentFont().info.ascender
		tempFont.info.descender = CurrentFont().info.descender
		tempFont.info.xHeight = CurrentFont().info.xHeight
		tempFont.info.capHeight = CurrentFont().info.capHeight

		tempFont.info.familyName = CurrentFont().info.familyName
		tempFont.info.styleName = CurrentFont().info.styleName

		tempFont.lib['com.robofont.robohint.cvt '] = CurrentFont().lib['com.robofont.robohint.cvt ']
		tempFont.lib['com.robofont.robohint.prep'] = CurrentFont().lib['com.robofont.robohint.prep']
		tempFont.lib['com.robofont.robohint.fpgm'] = CurrentFont().lib['com.robofont.robohint.fpgm']


		tempFont.newGlyph(self.g.name)
		tempFont[self.g.name] = tempGlyph

		tempFont.generate(self.tempfontpath, 'ttf', decompose = False, checkOutlines = False, autohint = False, releaseMode = True, glyphOrder=None, progressBar = None )


	def deleteTempFont(self):
		os.remove(self.tempfontpath)

	def loadGeneratedGlyphIntoLayer(self):
		tempUFO = OpenFont(self.tempfontpath, showUI=False)
		for temp_g in tempUFO:
			if temp_g.name == self.g.name:
				sourceLayer = temp_g.getLayer("foreground")
				targetLayer = self.g.getLayer("TTH_workingSpace")
				targetLayer.clear()
		 		targetWidth = self.g.width
		 		self.g.flipLayers("foreground", "TTH_workingSpace")
		 		self.f[self.g.name] = temp_g.copy()
		 		self.f[self.g.name].width = targetWidth
		 		self.g.update()


	def loadFaceGlyph(self):
		#freetype.get_handle()
		face = freetype.Face(self.tempfontpath)
		#face.set_char_size(size)
		face.set_pixel_sizes(int(self.PPM_Size), int(self.PPM_Size))
		#face.load_char(self.g.name)
		if self.wTools.boxView.monoCheckBox.get() == True:
			face.load_glyph(2, freetype.FT_LOAD_RENDER |
    	                    freetype.FT_LOAD_TARGET_MONO )
		elif self.wTools.boxView.grayCheckBox.get() == True:
			face.load_glyph(2, freetype.FT_LOAD_RENDER |
							freetype.FT_LOAD_TARGET_NORMAL)
		elif self.wTools.boxView.subpixelCheckBox.get() == True:
			face.load_glyph(2, freetype.FT_LOAD_RENDER |
                        freetype.FT_LOAD_TARGET_LCD )

		self.bitmap_buffer = face.glyph.bitmap.buffer
		self.bitmap_width  = face.glyph.bitmap.width
		self.bitmap_rows   = face.glyph.bitmap.rows
		self.bitmap_pitch  = face.glyph.bitmap.pitch
		self.bitmap_top    = face.glyph.bitmap_top
		self.bitmap_left   = face.glyph.bitmap_left

		self.outline_points = face.glyph.outline.points
		self.outline_tags = face.glyph.outline.tags
		self.outline_contours = face.glyph.outline.contours

		#print 'done exporting outline at size', size, UPM, pitch
		self.adaptedOutline_points = []
		for i in range(len(self.outline_points)):
			self.adaptedOutline_points.append( (int( self.pitch*self.outline_points[i][0]/64), int( self.pitch*self.outline_points[i][1]/64  )) )

		#return (adaptedOutline_points, outline_tags, outline_contours, bitmap_buffer, bitmap_width, bitmap_rows, bitmap_pitch)

	#################

	### TTH Tool Glyph Window ###

	def prepareGlyph(self):
		self.g = CurrentGlyph()

		myPen = self.g.getPen()
		myPen.moveTo((0, 0))
		myPen.closePath()
		myPen.moveTo((self.g.width, 0))
		myPen.closePath()
		self.g.update()

	def isOnPoint(self, p_cursor):
		def pred0(p_glyph):
			return pointsApproxEqual(p_glyph, p_cursor)
		touched_p_glyph = find_in_list(self.p_glyphList, pred0)

		return touched_p_glyph

	def getPointIndex(self, point):
		pastContoursLength = 0
		for c_index in range(len(self.g)):
			if c_index > 0:
				pastContoursLength += len(self.g[c_index-1].points)
			for p_index in range(len(self.g[c_index].points)):
				if self.g[c_index].points[p_index] == point:
					index = p_index + pastContoursLength
					return index
		return None

	def getPointByIndex(self, pointIndex):
		pastContoursLength = 0
		for c_index in range(len(self.g)):
			if c_index > 0:
				pastContoursLength += len(self.g[c_index-1].points)
			for p_index in range(len(self.g[c_index].points)):
				cp_index = p_index + pastContoursLength
				if pointIndex == cp_index:
					return self.g[c_index].points[p_index]
		return None

	def store_TTH_Set(self, TTH_Set):
		libName = "com.sansplomb.TTH_Sets"
		if libName in self.f.lib.keys():
			if self.g.name in self.f.lib[libName].keys():
				#store undo
				if self.g.name in self.undoStorage.keys():
					storeundo_glyphList = self.undoStorage[self.g.name]
					storeundo_glyphList.append(str(len(self.f.lib[libName][self.g.name].keys())))
					self.undoStorage[self.g.name] = storeundo_glyphList
				else:
					self.undoStorage[self.g.name] = [str(len(self.f.lib[libName][self.g.name].keys()))]
				#clear redostorage
				self.redoStorage[self.g.name] = []
				#store instruction
				self.f.lib[libName][self.g.name][str(len(self.f.lib[libName][self.g.name].keys()))] = (TTH_Set.axis, TTH_Set.set_type, TTH_Set.instructions)
			else:
				#store undo
				self.undoStorage[self.g.name] = [0]
				#print 'undo storage', self.undoStorage[self.g.name]
				#clear redostorage
				self.redoStorage[self.g.name] = []
				#store instruction
				self.f.lib[libName][self.g.name] = {}
				self.f.lib[libName][self.g.name]["0"] = (TTH_Set.axis, TTH_Set.set_type, TTH_Set.instructions)

		else:
			#store redostorage
			self.undoStorage[self.g.name] = ["0"]
			#clear redo
			self.redoStorage[self.g.name] = []
			#store instruction
			self.f.lib[libName] = {}
			self.f.lib[libName][self.g.name] = {}
			self.f.lib[libName][self.g.name]["0"] = (TTH_Set.axis, TTH_Set.set_type, TTH_Set.instructions)


	def read_TTH_Sets(self):
		libName = "com.sansplomb.TTH_Sets"
		if libName in self.f.lib.keys():
			if self.g.name in self.f.lib[libName].keys():
				#Set the axis of freedom and projection vectors
				Y_instructions = ['SVTCA[0]']
				X_instructions = ['SVTCA[1]']
				TTH_instructions = []
				for TTH_Set_index in self.f.lib[libName][self.g.name]:
					axis = self.f.lib[libName][self.g.name][TTH_Set_index][0]
					set_type = self.f.lib[libName][self.g.name][TTH_Set_index][1]
					set_instructions = self.f.lib[libName][self.g.name][TTH_Set_index][2]
					if axis == 'X':
						X_instructions.extend(set_instructions)
					elif axis == 'Y':
						Y_instructions.extend(set_instructions)
	
				TTH_instructions.extend(Y_instructions)
				TTH_instructions.extend(['IUP[0]'])
				TTH_instructions.extend(X_instructions)
				TTH_instructions.extend(['IUP[1]'])
				
				return TTH_instructions

		return None


	def write_TTH_Sets_ToGlyph(self, TTH_instructions):
		if 'com.robofont.robohint.assembly' in self.g.lib.keys():
			self.g.lib['com.robofont.robohint.assembly'].extend(TTH_instructions)
		else:
			self.g.lib['com.robofont.robohint.assembly'] = TTH_instructions


	def drawLink(self, scale, axis, startPoint, currentPoint):
	 	
	 	start_current_diff = difference(currentPoint, startPoint)
	 	dx, dy = -start_current_diff[1]/2, start_current_diff[0]/2
	 	offcurve1 = (startPoint.x + dx, startPoint.y + dy)
		offcurve2 = (currentPoint.x - dx, currentPoint.y - dy)
		r = 10
	 	arrowAngle = math.radians(20)
	 	initAngle = getAngle((currentPoint.x, currentPoint.y), (offcurve2[0], offcurve2[1]))
	 	arrowPoint1_x = currentPoint.x + math.cos(initAngle+arrowAngle)*r*scale
		arrowPoint1_y = currentPoint.y + math.sin(initAngle+arrowAngle)*r*scale
		arrowPoint2_x = currentPoint.x + math.cos(initAngle-arrowAngle)*r*scale
		arrowPoint2_y = currentPoint.y + math.sin(initAngle-arrowAngle)*r*scale
		endPoint_x = (arrowPoint1_x + arrowPoint2_x) / 2
		endPoint_y = (arrowPoint1_y + arrowPoint2_y) / 2

		pathArrow = NSBezierPath.bezierPath()
	 	pathArrow.moveToPoint_((currentPoint.x, currentPoint.y))
		pathArrow.lineToPoint_((arrowPoint1_x, arrowPoint1_y))
		pathArrow.lineToPoint_((arrowPoint2_x, arrowPoint2_y))


		path = NSBezierPath.bezierPath()
	 	path.moveToPoint_((startPoint.x, startPoint.y))
	 	path.curveToPoint_controlPoint1_controlPoint2_((endPoint_x,  endPoint_y), (offcurve1), (offcurve2) )

		#pathArrow.lineToPoint_((currentPoint.x, currentPoint.y))

	 	if axis == "X":
			NSColor.redColor().set()
		elif axis == "Y":
			NSColor.blueColor().set()
		path.setLineWidth_(scale)
		pathArrow.fill()
		path.stroke()

	def drawGrid(self, scale):
		for xPos in range(0, 4000, int(self.pitch)):
			pathX = NSBezierPath.bezierPath()
			pathX.moveToPoint_((xPos, -2000))
			pathX.lineToPoint_((xPos, 3000))
			NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 0.1).set()
			pathX.setLineWidth_(scale)
			pathX.stroke()
		for xPos in range(0, -4000, -int(self.pitch)):
			pathX = NSBezierPath.bezierPath()
			pathX.moveToPoint_((xPos, -2000))
			pathX.lineToPoint_((xPos, 3000))
			NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 0.1).set()
			pathX.setLineWidth_(scale)
			pathX.stroke()
		for yPos in range(0, 4000, int(self.pitch)):
			pathX = NSBezierPath.bezierPath()
			pathX.moveToPoint_((-2000, yPos))
			pathX.lineToPoint_((4000, yPos))
			NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 0.1).set()
			pathX.setLineWidth_(scale)
			pathX.stroke()
		for yPos in range(0, -4000, -int(self.pitch)):
			pathX = NSBezierPath.bezierPath()
			pathX.moveToPoint_((-2000, yPos))
			pathX.lineToPoint_((4000, yPos))
			NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 0.1).set()
			pathX.setLineWidth_(scale)
			pathX.stroke()

	def drawBitmapSubPixel(self):
		data = []
		for i in range(self.bitmap_rows):
			data.append(self.bitmap_buffer[i*self.bitmap_pitch:i*self.bitmap_pitch+self.bitmap_width])
		
		y = self.bitmap_top*self.pitch
		for row_index in range(len(data)):
			y -= self.pitch
			x = self.bitmap_left*self.pitch -self.pitch/3
			for pix_index in range(len(data[row_index])):
				x += self.pitch/3
				pix_color = data[row_index][pix_index]

				rect = NSBezierPath.bezierPath()
				rect.moveToPoint_((x, y))
				rect.lineToPoint_((x+self.pitch/3, y))
				rect.lineToPoint_((x+self.pitch/3, y+self.pitch))
				rect.lineToPoint_((x, y+self.pitch))
				rect.closePath
				NSColor.colorWithRed_green_blue_alpha_(0/255, 0/255, 0/255, .5*pix_color/255).set()
				rect.fill()	
				

	def drawBitmapGray(self):
		data = []
		for i in range(self.bitmap_rows):
			data.append(self.bitmap_buffer[i*self.bitmap_pitch:i*self.bitmap_pitch+self.bitmap_width])
		
		y = self.bitmap_top*self.pitch 
		for row_index in range(len(data)):
			y -= self.pitch
			x = self.bitmap_left*self.pitch -self.pitch
			for pix_index in range(len(data[row_index])):
				x += self.pitch
				pix_color = data[row_index][pix_index]

				rect = NSBezierPath.bezierPath()
				rect.moveToPoint_((x, y))
				rect.lineToPoint_((x+self.pitch, y))
				rect.lineToPoint_((x+self.pitch, y+self.pitch))
				rect.lineToPoint_((x, y+self.pitch))
				rect.closePath
				NSColor.colorWithRed_green_blue_alpha_(0/255, 0/255, 0/255, .5*pix_color/255).set()
				rect.fill()	

	def bits(self, x):
		data = []
		for i in range(8):
			data.insert(0, int((x & 1) == 1))
			x = x >> 1
		return data


	def drawBitmapMono(self):

		data = []
		for i in range(self.bitmap_rows):
			row = []
			for j in range(self.bitmap_pitch):
				row.extend(self.bits(self.bitmap_buffer[i*self.bitmap_pitch+j]))
			data.append(row[:self.bitmap_width])

		y = self.bitmap_top*self.pitch 
		for row_index in range(len(data)):
			y -= self.pitch
			x = self.bitmap_left*self.pitch -self.pitch
			for pix_index in range(len(data[row_index])):
				x += self.pitch
				pix_color = data[row_index][pix_index]

				rect = NSBezierPath.bezierPath()
				rect.moveToPoint_((x, y))
				rect.lineToPoint_((x+self.pitch, y))
				rect.lineToPoint_((x+self.pitch, y+self.pitch))
				rect.lineToPoint_((x, y+self.pitch))
				rect.closePath
				NSColor.colorWithRed_green_blue_alpha_(0/255, 0/255, 0/255, .5*pix_color).set()
				rect.fill()	

	def drawOutline(self, scale):
		#print outline.contours
		if len(self.outline_contours) == 0:
			return

		pathContour = NSBezierPath.bezierPath()
		start, end = 0, 0		
		for c_index in range(len(self.outline_contours)):
			end    = self.outline_contours[c_index]
			points = self.adaptedOutline_points[start:end+1] 
			points.append(points[0])
			tags   = self.outline_tags[start:end+1]
			tags.append(tags[0])

			segments = [ [points[0],], ]

			for j in range(1, len(points) ):
				segments[-1].append(points[j])
				if tags[j] & (1 << 0) and j < (len(points)-1):
					segments.append( [points[j],] )
			pathContour.moveToPoint_((points[0][0], points[0][1]))
			for segment in segments:
				if len(segment) == 2:
					pathContour.lineToPoint_(segment[1])
				else:
					onCurve = segment[0]
					for i in range(1,len(segment)-2):
						A,B = segment[i], segment[i+1]
						nextOn = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
						antenne1 = ((onCurve[0] + 2 * A[0]) / 3.0 , (onCurve[1] + 2 * A[1]) / 3.0)
						antenne2 = ((nextOn[0] + 2 * A[0]) / 3.0 , (nextOn[1] + 2 * A[1]) / 3.0)
						pathContour.curveToPoint_controlPoint1_controlPoint2_(nextOn, antenne1, antenne2)
						onCurve = nextOn
					nextOn = segment[-1]
					A = segment[-2]
					antenne1 = ((onCurve[0] + 2 * A[0]) / 3.0 , (onCurve[1] + 2 * A[1]) / 3.0)
					antenne2 = ((nextOn[0] + 2 * A[0]) / 3.0 , (nextOn[1] + 2 * A[1]) / 3.0)
					pathContour.curveToPoint_controlPoint1_controlPoint2_(nextOn, antenne1, antenne2)


			start = end+1

			NSColor.colorWithRed_green_blue_alpha_(0/255, 255/255, 255/255, .5).set()
			pathContour.setLineWidth_(scale)
			pathContour.stroke()

	def modifiersChanged(self):
		return self.getModifiers()["commandDown"]

	def keyDown(self, event):
		f = self.g.getParent()
		libName = "com.sansplomb.TTH_Sets"
		if self.modifiersChanged() and event.characters() == 'z':
			#UNDO action
			if len(self.undoStorage) != 0 and self.g.name in self.undoStorage.keys() and len(self.undoStorage[self.g.name]) != 0:
				#print 'undo glyph:', self.g.name
				#print 'undo instruction index:', self.undoStorage[self.g.name][len(self.undoStorage[self.g.name])-1]
				
				#prepare REDO
				deletedInstruction = f.lib[libName][self.g.name][str(self.undoStorage[self.g.name][len(self.undoStorage[self.g.name])-1])]
				deletedInstructionIndex = str(self.undoStorage[self.g.name][len(self.undoStorage[self.g.name])-1])

				self.redoStorage[self.g.name].append((deletedInstructionIndex, deletedInstruction))
				#print 'redo storage', self.redoStorage[self.g.name]
				#####

				del f.lib[libName][self.g.name][str(self.undoStorage[self.g.name][len(self.undoStorage[self.g.name])-1])]
				#print 'delete instruction index', str(self.undoStorage[self.g.name][len(self.undoStorage[self.g.name])-1])

				storeundo_glyphList = self.undoStorage[self.g.name]
				storeundo_glyphList.pop(len(self.undoStorage[self.g.name])-1)
				self.undoStorage[self.g.name] = storeundo_glyphList
			else:
				return

			self.g.flipLayers("foreground", "TTH_workingSpace")
			self.f.removeLayer("TTH_workingSpace")
			self.reset()


		if self.modifiersChanged() and event.characters() == 'y':
			if len(self.redoStorage[self.g.name]) != 0:
				f.lib[libName][self.g.name][str(len(f.lib[libName][self.g.name]))] = self.redoStorage[self.g.name][len(self.redoStorage[self.g.name])-1][1]
				self.redoStorage[self.g.name].pop(len(self.redoStorage[self.g.name])-1)

				storeundo_glyphList = self.undoStorage[self.g.name]
				storeundo_glyphList.append(str(len(self.undoStorage[self.g.name])))
				self.undoStorage[self.g.name] = storeundo_glyphList


			self.g.flipLayers("foreground", "TTH_workingSpace")
			self.f.removeLayer("TTH_workingSpace")

			TTH_instructions = self.read_TTH_Sets()
			if TTH_instructions != None:
				self.write_TTH_Sets_ToGlyph(TTH_instructions)

			self.reset()


		UpdateCurrentGlyphView()


	### Main Functions ###
	def becomeInactive(self):
		self.closeToolPanel()
		self.closeTablesPanel()

		self.g = CurrentGlyph()
		if self.g == None:
			return
		#self.g.removeContour(len(self.g)-1)
		#self.g.removeContour(len(self.g)-1)
		self.g.flipLayers("foreground", "TTH_workingSpace")
		self.f.removeLayer("TTH_workingSpace")

	def becomeActive(self):
		self.toolAxis = "Y"
		self.displayX = True
		self.displayY = True

		self.f = CurrentFont()
		self.g = CurrentGlyph()
		root =  os.path.split(self.f.path)[0]
		tail = 'temp.ttf'
		self.tempfontpath = os.path.join(root, tail)
		self.UPM = CurrentFont().info.unitsPerEm
		self.PPM_Size = 9
		self.pitch = self.UPM / self.PPM_Size

		self.previousGlyph  = None

		### Initialize currentTool ###

		self.currentTool = 'Link_RoundToGrid'

		#### Initializing CVT ####
		self.CVT_Index = []
		self.CVT_Names = []
		self.CVT_Values = []

		if 'com.robofont.robohint.cvt ' in self.f.lib.keys():
			self.CVT_Values = self.f.lib['com.robofont.robohint.cvt ']
			for i in range(len(self.f.lib['com.robofont.robohint.cvt '])):
				self.CVT_Index.append(i)
		if 'com.sansplomb.CVT_Names' in self.f.lib.keys():
			self.CVT_Names = self.f.lib['com.sansplomb.CVT_Names']


		self.CV_List = self.buidCVT_List(self.CVT_Index, self.CVT_Names, self.CVT_Values)

		if len(self.CV_List) > 0:
			self.selectedCV = (self.CV_List[0]["Index"], self.CV_List[0]["Name"], self.CV_List[0]["Value"])
		else:
			self.selectedCV = (None, None, None)

		#####################

		### Initializing FPGM #####
		self.FPGM = [	'PUSHB[ ] 0',
						'FDEF [ ]',
						'RCVT[ ]',
						'ROUND[01]',
						'WCVTP[ ]',
						'ENDF[ ]'
					]
		if 'com.robofont.robohint.fpgm' in self.f.lib.keys():
			self.FPGM = self.f.lib['com.robofont.robohint.fpgm']
		else:
			 self.f.lib['com.robofont.robohint.fpgm'] = self.FPGM

		####################

		### Initializing PREP #####
		self.PREP = [	'PUSHW[ ] 511',
						'SCANCTRL[ ]',
						'PUSHB[ ] 70',
						'SCVTCI[ ]',

						'MPPEM[ ]',
						'PUSHB[ ] 50',
						'GT[ ]',
						'IF[ ]',
						'PUSHB[ ] 128',
						'SCVTCI[ ]',
						'EIF[]',

						'PUSHB[ ] 0',
						'SZPS[]',

						'PUSHB[ ] 0 1',
						'MIAP[1]'


					]


		if 'com.robofont.robohint.prep' in self.f.lib.keys():
			self.PREP = self.f.lib['com.robofont.robohint.prep']
		else:
			 self.f.lib['com.robofont.robohint.prep'] = self.PREP

		####################


		### THTool Panel ###
		self.wTools = FloatingWindow((10, 30, 170, 600), "TTH ToolBar", closable = False)
		self.PPMSizesList = ['9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 
							'21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
							'31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
							'41', '42', '43', '44', '45', '46', '47', '48', '60', '72' ]

		self.wTools.PPEMSizeText= TextBox((10, 10, 70, 14), "PPEM Size:", sizeStyle = "small")
		
		self.wTools.PPEMSizeEditText = EditText((80, 8, 30, 19), sizeStyle = "small", 
                            callback=self.PPEMSizeEditTextCallback)
		self.wTools.PPEMSizeEditText.set(self.PPM_Size)
		
		self.wTools.PPEMSizePopUpButton = PopUpButton((120, 10, 40, 14),
                              self.PPMSizesList, sizeStyle = "small",
                              callback=self.PPEMSizePopUpButtonCallback)

		self.wTools.textTool= TextBox((10, 34, 70, 14), "Tool Axis", sizeStyle = "small")
		self.wTools.boxTool = Box((10, 54, 70, 70))
		self.wTools.boxTool.yToolCheckBox = CheckBox((10, 10, 50, 20), "Y", callback=self.yToolCheckBoxCallback, value=True)
		self.wTools.boxTool.xToolCheckBox = CheckBox((10, 30, 50, 20), "X", callback=self.xToolCheckBoxCallback, value=False)

		self.wTools.textDisplay= TextBox((90, 34, 70, 14), "View Axis", sizeStyle = "small")
		self.wTools.boxDisplay = Box((90, 54, 70, 70))
		self.wTools.boxDisplay.yDisplayCheckBox = CheckBox((10, 10, 50, 20), "Y", callback=self.yDisplayCheckBoxCallback, value=True)
		self.wTools.boxDisplay.xDisplayCheckBox = CheckBox((10, 30, 50, 20), "X", callback=self.xDisplayCheckBoxCallback, value=True)

		self.wTools.textTools= TextBox((10, 134, 70, 14), "Tools", sizeStyle = "small")
		self.wTools.boxTools = Box((10, 154, 150, 110))
		self.wTools.boxTools.linkCheckBox = CheckBox((10, 10, 50, 20), "Link", callback=self.linkCheckBoxCallback, value=True)
		self.wTools.boxTools.interpolateCheckBox = CheckBox((10, 30, 100, 20), "Interpolate", callback=self.interpolateCheckBoxCallback, value=False)
		self.wTools.boxTools.middleDeltaCheckBox = CheckBox((10, 50, 100, 20), "Middle Delta", callback=self.middleDeltaCheckBoxCallback, value=False)
		self.wTools.boxTools.finalDeltaCheckBox = CheckBox((10, 70, 100, 20), "Final Delta", callback=self.finalDeltaCheckBoxCallback, value=False)
		self.wTools.buttonShowTablesPanel = Button((10, 270, -10, 22), "Show Tables Panel", sizeStyle = 'small', 
                            callback=self.buttonShowTablesPanelCallback)
		self.wTools.buttonHideTablesPanel = Button((10, 270, -10, 22), "Hide Tables Panel", sizeStyle = 'small', 
                            callback=self.buttonHideTablesPanelCallback)
		self.wTools.buttonHideTablesPanel.show(False)

		self.wTools.textView= TextBox((10, 300, 70, 14), "Preview", sizeStyle = "small")
		self.wTools.boxView = Box((10, 320, 150, 90))
		self.wTools.boxView.monoCheckBox = CheckBox((10, 10, -10, 20), "Monochrome", callback=self.monoCheckBoxCallback, value=True)
		self.wTools.boxView.grayCheckBox = CheckBox((10, 30, -10, 20), "Grayscale", callback=self.grayCheckBoxCallback, value=False)
		self.wTools.boxView.subpixelCheckBox = CheckBox((10, 50, -10, 20), "Subpixel", callback=self.subpixelCheckBoxCallback, value=False)

		self.wTools.open()
		
		######################

		self.wTables = FloatingWindow((182, 30, 270, 400), "TTH Tables", closable = False, initiallyVisible=False)
		self.wTables.textTool= TextBox((10, 10, 70, 14), "CVT", sizeStyle = "small")
		self.wTables.boxCVT = Box((10, 34, 250, 150))
		self.wTables.boxCVT.CVT_List = List((0, 0, -0, 100),
                     self.CV_List,
                     columnDescriptions=[{"title": "Index", "editable": False}, {"title": "Name", "editable": True}, {"title": "Value", "editable": True}],
                     selectionCallback=self.CVT_SelectionCallback, 
                     editCallback=self.CVT_EditCallBack)
		self.wTables.boxCVT.buttonRemoveCV = SquareButton((0, 100, 22, 22), "-", sizeStyle = 'small', 
                            callback=self.buttonRemoveCVCallback)
		self.wTables.boxCVT.editTextCV_Name = EditText((22, 100, 120, 22),
                            callback=self.editTextCV_NameCallback)
		self.wTables.boxCVT.editTextCV_Value = EditText((142, 100, -22, 22),
                            callback=self.editTextCV_ValueCallback)
		self.wTables.boxCVT.buttonAddCV = SquareButton((-22, 100, 22, 22), u"↵", sizeStyle = 'small', 
                            callback=self.buttonAddCVCallback)
		
		self.wTables.open()
		self.wTables.hide()

		#####################

		if self.g == None:
			return
		self.generateTempFont()

	def reset(self):

		self.generateTempFont()
		self.loadGeneratedGlyphIntoLayer()
		self.prepareGlyph()
		self.loadFaceGlyph()
		UpdateCurrentGlyphView()

		self.p_glyphList = []
		self.startPoint = None
		self.endPoint = None

		for c in self.g:
			for p in c.points:
				if p.type != 'offCurve':
					self.p_glyphList.append(p)
		self.g.update()

		self.currentTool = None
		self.controlValueIndex = None

	def viewWillChangeGlyph(self):
		if self.g == None:
			return
		self.previousGlyph = self.g		

	def viewDidChangeGlyph(self):

		if self.previousGlyph != None:
			#self.previousGlyph.removeContour(len(self.previousGlyph)-1)
			#self.previousGlyph.removeContour(len(self.previousGlyph)-1)
			self.previousGlyph.flipLayers("foreground", "TTH_workingSpace")
			self.f.removeLayer("TTH_workingSpace")

		self.g = CurrentGlyph()
		self.f = CurrentFont()
		if self.g == None:
			return

		TTH_instructions = self.read_TTH_Sets()
		if TTH_instructions != None:
			self.write_TTH_Sets_ToGlyph(TTH_instructions)

		self.reset()

	def mouseDown(self, point, clickCount):

		self.p_cursor = (int(point.x), int(point.y))
		self.startPoint = self.isOnPoint(self.p_cursor)
		self.controlValueIndex = None
		self.currentTool = None

	def roundToGridCallback(self, controlValue):
		self.currentTool = 'Link_RoundToGrid'
		self.controlValueIndex = None

	def mouseUp(self, point):

		self.p_cursor = (int(point.x), int(point.y))
		self.endPoint = self.isOnPoint(self.p_cursor)

		#print self.startPoint, self.endPoint

		if self.startPoint != self.endPoint and self.startPoint != None and self.endPoint != None:
			#print 'touched'
			inPointIndex = self.getPointIndex(self.startPoint)
			outPointIndex = self.getPointIndex(self.endPoint)
			#print inPointIndex, outPointIndex
			if outPointIndex != None and inPointIndex != None:
				#### Pre-sets for Hint type and CV ###
				
				#self.instructionType = 'link'
				######################################	

				self.menuCVT = NSMenu.alloc().init()
				separator = NSMenuItem.separatorItem()
				items = []
				items.append(('Round To Grid', self.roundToGridCallback))
				
				controlValuesList = self.generateMenuItemsList(self.CV_List)
				for i in controlValuesList:
					self.c_title = i[1] + ' @ ' + str(i[2])
					self.c_callback = CallBackCVT(i, self)
					items.append((self.c_title, self.c_callback))

				menuController = BaseMenu()
				menuController.buildAdditionContectualMenuItems(self.menuCVT, items)
				self.menuCVT.insertItem_atIndex_(separator, 1)
				NSMenu.popUpContextMenu_withEvent_forView_(self.menuCVT, self.getCurrentEvent(), self.getNSView())

				if self.controlValueIndex != None:
					print 'CV Selected index:', self.controlValueIndex, inPointIndex, outPointIndex
					instructions = ['PUSHW[ ] ' + str(inPointIndex),
									'MDAP[1]',
									'PUSHW[ ] ' + str(outPointIndex),
									'PUSHB[ ] ' + str(self.controlValueIndex),
									'MIRP[00101]'
									]
					c_Link_CVT = TTH_Set(self.toolAxis, self.currentTool, instructions)
					self.store_TTH_Set(c_Link_CVT)
					TTH_instructions = self.read_TTH_Sets()
					print TTH_instructions
					self.write_TTH_Sets_ToGlyph(TTH_instructions)

					self.g.flipLayers("foreground", "TTH_workingSpace")
					self.f.removeLayer("TTH_workingSpace")
					self.reset()

				elif self.currentTool == 'Link_RoundToGrid':
					print 'Link_RoundToGrid'

					instructions = [
									'PUSHW[ ] ' + str(inPointIndex),
									'MDAP[1]',
									'PUSHW[ ] ' + str(outPointIndex),
									'MDRP[00100]'
									]

					c_Link_RountToGrid = TTH_Set(self.toolAxis, self.currentTool, instructions)
					self.store_TTH_Set(c_Link_RountToGrid)

					TTH_instructions = self.read_TTH_Sets()
					print TTH_instructions
					self.write_TTH_Sets_ToGlyph(TTH_instructions)

					self.g.flipLayers("foreground", "TTH_workingSpace")
					self.f.removeLayer("TTH_workingSpace")
					self.reset()

	def draw(self, scale):
		if self.isDragging() and self.startPoint != None:
			r = 5*scale
			x_start = self.startPoint.x
			y_start = self.startPoint.y

			NSColor.colorWithRed_green_blue_alpha_(0, 1, 1, .5).set()
			NSBezierPath.bezierPathWithOvalInRect_(((x_start-r, y_start-r), (r*2, r*2))).fill()

			self.drawLink(scale, self.toolAxis, self.startPoint, self.currentPoint)

			touchedEnd = self.isOnPoint(self.currentPoint)
			if touchedEnd != None:
				x_end = touchedEnd.x
				y_end = touchedEnd.y
				NSColor.colorWithRed_green_blue_alpha_(0, 1, 1, .5).set()
				NSBezierPath.bezierPathWithOvalInRect_(((x_end-r, y_end-r), (r*2, r*2))).fill()

		if self.f.lib and "com.sansplomb.TTH_Sets" in self.f.lib.keys() and self.g.name in self.f.lib["com.sansplomb.TTH_Sets"].keys():
			for key in self.f.lib["com.sansplomb.TTH_Sets"][self.g.name].keys():
				(axis, set_type, instructions)= self.f.lib["com.sansplomb.TTH_Sets"][self.g.name][key]
				if set_type == 'Link_RoundToGrid':
					inPointIndex = int(instructions[0].split(' ')[-1:][0])
					outPointIndex = int(instructions[2].split(' ')[-1:][0])
					if self.displayX == True and self.displayY == True:
						self.drawLink(scale, axis, self.getPointByIndex(inPointIndex), self.getPointByIndex(outPointIndex))

					elif self.displayY == False and self.displayX == True and axis == 'X':
						self.drawLink(scale, axis, self.getPointByIndex(inPointIndex), self.getPointByIndex(outPointIndex))

					elif self.displayX == False and self.displayY == True and axis == 'Y':
						self.drawLink(scale, axis, self.getPointByIndex(inPointIndex), self.getPointByIndex(outPointIndex))

				if set_type == 'Link_CVT':
					inPointIndex = int(instructions[0].split(' ')[-1:][0])
					outPointIndex = int(instructions[2].split(' ')[-1:][0])
					if self.displayX == True and self.displayY == True:
						self.drawLink(scale, axis, self.getPointByIndex(inPointIndex), self.getPointByIndex(outPointIndex))

					elif self.displayY == False and self.displayX == True and axis == 'X':
						self.drawLink(scale, axis, self.getPointByIndex(inPointIndex), self.getPointByIndex(outPointIndex))

					elif self.displayX == False and self.displayY == True and axis == 'Y':
						self.drawLink(scale, axis, self.getPointByIndex(inPointIndex), self.getPointByIndex(outPointIndex))
						
					


		

	def drawBackground(self, scale):
		#self.drawBitmap()
		if self.wTools.boxView.monoCheckBox.get() == True:
			self.drawBitmapMono()
		elif self.wTools.boxView.grayCheckBox.get() == True:
			self.drawBitmapGray()
		elif self.wTools.boxView.subpixelCheckBox.get() == True:
			self.drawBitmapSubPixel()

		self.drawGrid(scale)	
		self.drawOutline(scale)	

		r = 5*scale
		x = 0
		y = 0
		NSColor.colorWithRed_green_blue_alpha_(1, 0, 0, 1).set()
		NSBezierPath.bezierPathWithOvalInRect_(((x-r, y-r), (r*2, r*2))).fill()
		x = self.g.width
		y = 0
		NSColor.colorWithRed_green_blue_alpha_(1, 0, 0, 1).set()
		NSBezierPath.bezierPathWithOvalInRect_(((x-r, y-r), (r*2, r*2))).fill()


	### TTHTool Panel Callbacks ###
	def PPEMSizeEditTextCallback(self, sender):
		try:
			newValue = int(sender.get())
		except ValueError:
			newValue = 1
			sender.set(1)
		self.PPM_Size = newValue
		self.pitch = int(self.UPM / int(self.PPM_Size))
		self.loadFaceGlyph()
		UpdateCurrentGlyphView()

	def PPEMSizePopUpButtonCallback(self, sender):
		self.PPM_Size = self.PPMSizesList[sender.get()]
		self.wTools.PPEMSizeEditText.set(self.PPM_Size)
		self.pitch = int(self.UPM / int(self.PPM_Size))
		self.loadFaceGlyph()
		UpdateCurrentGlyphView()

	def yToolCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.toolAxis = "Y"
			self.wTools.boxTool.xToolCheckBox.set(False)

	def xToolCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.toolAxis = "X"
			self.wTools.boxTool.yToolCheckBox.set(False)

	def yDisplayCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.displayY = True
		else:
			self.displayY = False
		UpdateCurrentGlyphView()

	def xDisplayCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.displayX = True
		else:
			self.displayX = False
		UpdateCurrentGlyphView()

	def linkCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.wTools.boxTools.interpolateCheckBox.set(False)
			self.wTools.boxTools.middleDeltaCheckBox.set(False)
			self.wTools.boxTools.finalDeltaCheckBox.set(False)

	def interpolateCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.wTools.boxTools.linkCheckBox.set(False)
			self.wTools.boxTools.middleDeltaCheckBox.set(False)
			self.wTools.boxTools.finalDeltaCheckBox.set(False)

	def middleDeltaCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.wTools.boxTools.linkCheckBox.set(False)
			self.wTools.boxTools.interpolateCheckBox.set(False)
			self.wTools.boxTools.finalDeltaCheckBox.set(False)

	def finalDeltaCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.wTools.boxTools.linkCheckBox.set(False)
			self.wTools.boxTools.interpolateCheckBox.set(False)
			self.wTools.boxTools.middleDeltaCheckBox.set(False)

	def buttonShowTablesPanelCallback(self, sender):
		self.wTables.show()
		self.wTools.buttonShowTablesPanel.show(False)
		self.wTools.buttonHideTablesPanel.show(True)

	def buttonHideTablesPanelCallback(self, sender):
		self.wTables.hide()
		self.wTools.buttonShowTablesPanel.show(True)
		self.wTools.buttonHideTablesPanel.show(False)

	def monoCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.wTools.boxView.grayCheckBox.set(False)
			self.wTools.boxView.subpixelCheckBox.set(False)
		self.loadFaceGlyph()
		UpdateCurrentGlyphView()

	def grayCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.wTools.boxView.monoCheckBox.set(False)
			self.wTools.boxView.subpixelCheckBox.set(False)
		self.loadFaceGlyph()
		UpdateCurrentGlyphView()

	def subpixelCheckBoxCallback(self, sender):
		if sender.get() == 1:
			self.wTools.boxView.grayCheckBox.set(False)
			self.wTools.boxView.monoCheckBox.set(False)
		self.loadFaceGlyph()
		UpdateCurrentGlyphView()


	def closeToolPanel(self):
		self.wTools.close()

	def openToolPanel(self):
		self.wTools.open()
	#####################

	### TTHTables Panel CallBacks ###
	def buidCVT_List(self, CVT_Index, CVT_Names, CVT_Values):
		CVZip = map(None, CVT_Index, CVT_Names, CVT_Values)
		CV_List = []
		for index, name, value in CVZip:
			CVT_dict = {}
			CVT_dict['Index'] = index
			if name == None or name =='':
				CVT_dict['Name'] = 'Untitled'
			else:
				CVT_dict['Name'] = name
			CVT_dict['Value'] = value
			CV_List.append(CVT_dict)
		return CV_List

	def generateMenuItemsList(self, CV_List):
		itemsList = []
		for i in CV_List:
			index = i['Index']
			name = i['Name']
			value = int(i['Value'])
			itemsList.append((index, name, value))
		return itemsList

	def CVT_SelectionCallback(self, sender):
		self.selectedCV = None
		if len(sender.getSelection()) != 0:
			self.selectedCV = (self.CV_List[sender.getSelection()[0]]["Index"], self.CV_List[sender.getSelection()[0]]["Name"], self.CV_List[sender.getSelection()[0]]["Value"] )
		#print self.selectedCV

	def CVT_EditCallBack(self, sender):
		indexesList = []
		namesList = []
		valuesList = []

		self.CV_List = sender.get()

		for entry in self.CV_List:
			indexesList.append(entry['Index'])
			if entry['Name'] == None:
				namesList.append('Untitled')
			else:
				namesList.append(entry['Name'])
			valuesList.append(int(entry['Value']))

		self.CVT_Index = indexesList
		self.f.lib['com.sansplomb.CVT_Names'] = namesList
		self.CVT_Names = namesList

		self.CVT_Values = valuesList
		self.f.lib['com.robofont.robohint.cvt '] = valuesList

	def buttonRemoveCVCallback(self, sender):
		if self.selectedCV == None:
			return
		index = self.selectedCV[0]
		name = self.selectedCV[1]
		value = self.selectedCV[2]

		self.f.lib['com.robofont.robohint.cvt '].pop(index)
		self.f.lib['com.sansplomb.CVT_Names'].pop(index)
		for i in range(len(self.CVT_Index)):
			if i>index:
				self.CVT_Index[i] -= 1
		self.CVT_Index.pop(index)

		self.CV_List = self.buidCVT_List(self.CVT_Index, self.f.lib['com.sansplomb.CVT_Names'], self.f.lib['com.robofont.robohint.cvt '])
		self.wTables.boxCVT.CVT_List.set(self.CV_List)


	def editTextCV_NameCallback(self, sender):
		sender.get()

	def editTextCV_ValueCallback(self, sender):
		try:
			value = int(sender.get())
		except ValueError:
			value = 0
			sender.set(0)

	def buttonAddCVCallback(self, sender):
		index = 0
		if 'com.robofont.robohint.cvt ' in self.f.lib.keys():
			index = len( self.f.lib['com.robofont.robohint.cvt '] )

		name = self.wTables.boxCVT.editTextCV_Name.get()
		value = int(self.wTables.boxCVT.editTextCV_Value.get())
		if name != '' and value != '':
			self.CVT_Index.append(index)
			if 'com.sansplomb.CVT_Names' in self.f.lib.keys():
				self.f.lib['com.sansplomb.CVT_Names'].append(name)
			else:
				self.f.lib['com.sansplomb.CVT_Names'] = [name]
			if 'com.robofont.robohint.cvt ' in self.f.lib.keys():
				self.f.lib['com.robofont.robohint.cvt '].append(value)
			else:
				self.f.lib['com.robofont.robohint.cvt '] = [value]

		self.CV_List = self.buidCVT_List(self.CVT_Index, self.f.lib['com.sansplomb.CVT_Names'], self.f.lib['com.robofont.robohint.cvt '])

		self.wTables.boxCVT.CVT_List.set(self.CV_List)

	def closeTablesPanel(self):
		self.wTables.close()

	#####################



installTool(TTHTool())