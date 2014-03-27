from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController


class Process(BaseWindowController):

	def __init__(self):
		self.w = FloatingWindow((310, 170))
		self.w.textBox = TextBox((10, 10, -10, 16), "Glyphs Integrity Check", sizeStyle = "regular", alignment = "center")
		self.w.checkBoxMixedContours = CheckBox((10, 40, -10, 20), "Mixed Contours and Components", sizeStyle = "small", 
											callback=self.checkBoxMixedContoursCallback, value = False)
		self.w.checkBoxOverlappingComponents = CheckBox((10, 70, -10, 20), "Overlapping Components", sizeStyle = "small", 
											callback=self.checkBoxOverlappingComponentsCallback, value = False)
		self.w.checkBoxOverlap = CheckBox((10, 100, -10, 20), "Overlapping Contours", sizeStyle = "small", 
											callback=self.checkBoxOverlapCallback, value = False)
		self.w.buttonCheck = Button((10, -20, 190, 15), "Check", sizeStyle = "small", callback=self.showProgress)
		self.w.buttonClose = Button((210, -20, 90, 15), "Close", sizeStyle = "small", callback=self.closeWindow)
		self.w.center()
		self.w.open()
		
	def closeWindow(self, sender):
		self.w.close()
	
	def checkBoxMixedContoursCallback(self, sender):
		sender.get()
		#	self.w.checkBoxOverlappingComponents.set(False)
		#	self.w.checkBoxOverlap.set(False)
		
	def checkBoxOverlappingComponentsCallback(self, sender):
		sender.get()
		#	self.w.checkBoxMixedContours.set(False)
		#	self.w.checkBoxOverlap.set(False)
	
	def checkBoxOverlapCallback(self, sender):
		sender.get()
		#	self.w.checkBoxMixedContours.set(False)
		#	self.w.checkBoxOverlappingComponents.set(False)
	
	def showProgress(self, sender):
		if self.w.checkBoxMixedContours.get():
			self.progress = self.startProgress("Checking Mixed...")
			self.checkMixedContours(f)
			self.progress.close()
			
		if self.w.checkBoxOverlappingComponents.get():
			self.progress = self.startProgress("Checking Overlapping Components...")
			self.checkOverlappingComponents(f)
			self.progress.close()
			
		if self.w.checkBoxOverlap.get():
			self.progress = self.startProgress("Checking Overlapping contours...")
			self.checkOverlap(f)
			self.progress.close()
		self.w.close()
	
	def checkMixedContours(self, f):
		self.progress.setTickCount(len(f))
		print '-----------------------------------'
		print 'Mixed Contours and Composite Report'
		print '-----------------------------------'
		for g in f:
			self.progress.update()
			if g.components:
				if len(g) > 0:
					print g.name, 'has mixed contour and composite'
					g.mark = (0.5, 0, 0, 0.4)
		f.update()
			
	def checkOverlappingComponents(self, f):
		self.progress.setTickCount(len(f))
		print '----------------------------'
		print 'Overlapping Components Report'
		print '----------------------------'
		for g in f:
			self.progress.update()
			if g.components:
				pDM_list = []
				pD_list = []
				g.getLayer("_backupDecMerg").clear()
				g.copyToLayer("_backupDecMerg")
				g.getLayer("_backupDec").clear()
				g.copyToLayer("_backupDec")
				gDecomposedMerged = g.getLayer("_backupDecMerg")
				gDecomposed = g.getLayer("_backupDec")	
				for cp in gDecomposedMerged.components:
					gDecomposedMerged.decompose()
					gDecomposed.decompose()
				gDecomposedMerged.removeOverlap()
				#if len(gDecomposedMerged) != len(gDecomposed):
				for cDM_index in range(len(gDecomposedMerged)):
					for i in range(len(gDecomposedMerged[cDM_index])):
						pDM_list.append(i)
				for cD_index in range(len(gDecomposed)):
					for i in range(len(gDecomposed[cD_index])):
						pD_list.append(i)
				if len(pDM_list) != len(pD_list) or len(gDecomposedMerged) != len(gDecomposed):
					print g.name, 'has overlapping components'
					g.mark = (0.5, 0, 0, 0.4)
		f.removeLayer("_backupDecMerg")
		f.removeLayer("_backupDec")
		f.update()
	
	def checkOverlap(self, f):
		self.progress.setTickCount(len(f))
		print '--------------------------'
		print 'Overlapping Contours Report'
		print '--------------------------'
		for g in f:
			self.progress.update()
			pg_List = []
			pgMerged_List = []
			g.getLayer("_backupMerged").clear()
			g.copyToLayer("_backupMerged")
			gMerged = g.getLayer("_backupMerged")
			gMerged.removeOverlap()
			for i in range(len(g)):
				for j in range(len(g[i])):
					pg_List.append(j)
			for i in range(len(gMerged)):
				for j in range(len(gMerged[i])):
					pgMerged_List.append(j)
			if len(pg_List) != len(pgMerged_List):
					print g.name, 'has overlapping contours'
					g.mark = (0.5, 0, 0, 0.4)
		
		f.removeLayer("_backupMerged")
		f.update()


f = CurrentFont()
Process()
