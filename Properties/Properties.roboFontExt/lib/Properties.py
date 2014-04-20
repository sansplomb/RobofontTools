#coding=utf-8

from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver

class ShowPropertiesTextBox(TextBox):
	def __init__(self, *args, **kwargs):
		super(ShowPropertiesTextBox, self).__init__(*args, **kwargs)
		addObserver(self, "draw", "draw")
		
	def getDist(self, a_list):
		if a_list:
			return max(a_list) - min(a_list)
		else:
			return 0
	
	def getOffSelection(self):
		for contour in CurrentGlyph():
			for s in range(len(contour)):
				for point in contour[s]:
					if point.selected and point.type == 'offCurve':
						return (contour, s, point)
		return None
	
	def getOnsSelected(self):
		contourList = []
		onPointList = []
		offPointList = []
		list_x = []
		list_y = []
		for contour in CurrentGlyph():
			contourList.append(contour)
			for segment in contour:
				for point in segment:
					if point.type != 'offCurve':
						onPointList.append(point)
					elif point.type == 'offCurve':
						offPointList.append(point)
					if point.selected:
						list_x.append(point.x)
						list_y.append(point.y)
		
		return (list_x, list_y, contourList, onPointList, offPointList)
	
	def bcpDistance(self):
		sel = self.getOffSelection()
		if sel == None:
			return (0, 0)

		con, segIdx, pt = sel
		seg = con[segIdx]
		onPt = pt

		if pt == seg.offCurve[-1]: # 'Incoming'
			onPt = seg.onCurve 
		elif pt == seg.offCurve[0]: # 'Outcoming'
			onPt = con[segIdx-1].onCurve
		dx = pt.x - onPt.x
		dy = pt.y - onPt.y
		return (dx, dy)
		
	def onSelectedDistance(self):
		(list_x, list_y, contourList, onPointList, offPointList) = self.getOnsSelected()
		dist_x = self.getDist(list_x)
		dist_y = self.getDist(list_y)
		return (dist_x, dist_y, len(contourList), len(onPointList), len(offPointList))
	
	
	def draw(self, info):
		CurrentGlyph().update()
		(bcpDist_x, bcpDist_y) = self.bcpDistance()
		(dist_x, dist_y, contours, onPoints, offPoints) = self.onSelectedDistance()
				
		text = u"⥓ %s ⥔ %s | ↔︎ %s ↕︎ %s | ◦ %s ⋅ %s ⟜ %s" % (bcpDist_x, bcpDist_y, dist_x, dist_y, contours, onPoints, offPoints)
		self.set(text)
		
		def windowCloseCallback(self, sender):
			super(ShowPropertiesTextBox, self).windowCloseCallback(sender)
			removeObserver(self, "draw")
		
		
class ShowProperties(BaseWindowController):
	def __init__(self):
		addObserver(self, "glyphWindowDidOpen", "glyphWindowDidOpen")
	
	def glyphWindowDidOpen(self, info):
		window = info["window"]
		vanillaView = ShowPropertiesTextBox((20, 22, -20, 22), "", alignment="right", sizeStyle="mini")
		superview = window.editGlyphView.enclosingScrollView().superview()
		view = vanillaView.getNSTextField()
		frame = superview.frame()
		vanillaView._setFrame(frame)
		superview.addSubview_(view)
		
	def windowCloseCallback(self, sender):
		super(ShowPropertiesTextBox, self).windowCloseCallback(sender)
		removeObserver(self, "glyphWindowDidOpen")

ShowProperties()