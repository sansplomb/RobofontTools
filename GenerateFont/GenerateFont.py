from vanilla import *
from fontTools import *
from mojo.events import *
from defconAppKit.windows.baseWindow import BaseWindowController
from os import *


class GenerateWindow(BaseWindowController):

	def __init__(self):
		
		addObserver(self, "fontGenerated", "fontDidGenerate")
		
		self.decompose = False
		self.checkOutlines = False
		self.autohint = False
		self.releaseMode = False
		self.writeKern = False
		self.expandKern = False
		self.formatList = ["otf", "ttf"]
		self.formatIndex = 0
		self.formatName = "otf"
		
		self.w = FloatingWindow((310, 200), "Generate Font")
	
		self.w.formatTextBox = TextBox((10, 10, 100, 20), "Format")
		self.w.popUpButtonFormat = PopUpButton((10, 30, 100, 20),
							  self.formatList, sizeStyle = "small", callback=self.popUpButtonFormatCallback)
							  
		self.w.checkBoxDecompose = CheckBox((10, 60, 150, 20), "Decompose", sizeStyle = "small", 
											callback=self.checkBoxDecomposeCallback, value = False)
		self.w.checkBoxRemoveOverlap = CheckBox((10, 80, 150, 20), "Remove Overlap", sizeStyle = "small", 
											callback=self.checkBoxRemoveOverlapCallback, value = False)
		self.w.checkBoxAutoHint = CheckBox((10, 100, 150, 20), "AutoHint", sizeStyle = "small", 
											callback=self.checkBoxAutoHintCallback, value = False)
		self.w.checkBoxReleaseMode = CheckBox((10, 120, 150, 20), "Release Mode", sizeStyle = "small", 
											callback=self.checkBoxReleaseModeCallback, value = False)
											
		self.w.checkBoxWriteKern = CheckBox((160, 60, -10, 20), "Write Kern Table", sizeStyle = "small", 
											callback=self.checkBoxWriteKernCallback, value = False)
		self.w.checkBoxExpandKerning = CheckBox((160, 80, -10, 20), "Expand Class Kerning", sizeStyle = "mini", 
											callback=self.checkBoxExpandKerningCallback, value = False)
		self.w.checkBoxExpandKerning.show(0)
		
											
		self.w.buttonGenerate = Button((10, -25, 90, 15), "Generate", sizeStyle = "small", callback=self.generateFont)
		self.w.buttonGenerateAll = Button((110, -25, 90, 15), "Generate All", sizeStyle = "small", callback=self.generateAllFonts)
		self.w.buttonClose = Button((210, -25, 90, 15), "Close", sizeStyle = "small", callback=self.closeWindow)
		
		
		self.w.center()
		self.showGetFolder(callback=self.openFolderCallBack)

		self.w.open()
		
	
	def closeWindow(self, sender):
		removeObserver(self, "fontgenerated")
		self.w.close()
		
			
	def popUpButtonFormatCallback(self, sender):
		self.formatIndex == sender.get()
		self.formatName = self.formatList[sender.get()]
				
	def checkBoxDecomposeCallback(self, sender):
		if sender.get() == 0:
			self.decompose = False
		else:
			self.decompose = True
				
	def checkBoxRemoveOverlapCallback(self, sender):
		if sender.get() == 0:
			self.checkOutlines = False
		else:
			self.checkOutlines = True
		
	def checkBoxAutoHintCallback(self, sender):
		if sender.get() == 0:
			self.autohint = False
		else:
			self.autohint = True
	
	def checkBoxReleaseModeCallback(self, sender):
		if sender.get() == 0:
			self.releaseMode = False
		else:
			self.releaseMode = True
		
	def checkBoxWriteKernCallback(self, sender):
		if sender.get() == 0:
			self.writeKern = False
		else:
			self.writeKern = True
		self.w.checkBoxExpandKerning.show(sender.get())
	
	def checkBoxExpandKerningCallback(self, sender):
		if sender.get() == 0:
			self.expandKern = False
		else:
			self.expandKern = True
	
	def generateFont(self, sender):
		self.fontName = ''
		familyNameList = f.info.openTypeNamePreferredFamilyName.split(' ')
		for i in familyNameList:
			self.fontName += i
		self.fontName += '-' + f.info.openTypeNamePreferredSubfamilyName + '.' + self.formatName
		
		self.fontpath = path.join(self.savingfolderpath, self.fontName)		
		print self.fontpath
		
		self.progress = self.startProgress()

		f.generate(self.fontpath, self.formatName, self.decompose, self.checkOutlines, self.autohint, self.releaseMode, glyphOrder=None, progressBar = self.progress)
		self.progress.close()
		if self.writeKern == True:
			self.addKerntable(f)
		
		
	def generateAllFonts(self, sender):
		for f in af:
			self.fontName = ''
			familyNameList = f.info.openTypeNamePreferredFamilyName.split(' ')
			for i in familyNameList:
				self.fontName += i
			self.fontName += '-' + f.info.openTypeNamePreferredSubfamilyName + '.' + self.formatName
		
			self.fontpath = path.join(self.savingfolderpath, self.fontName)		
			print self.fontpath
		
			self.progress = self.startProgress()

			f.generate(self.fontpath, self.formatName, self.decompose, self.checkOutlines, self.autohint, self.releaseMode, glyphOrder=None, progressBar = self.progress)
			self.progress.close()
			if self.writeKern == True:
				self.addKerntable(f)
			
			
	def openFolderCallBack(self, sender):
		self.savingfolderpath = sender[0]
		
	def addKerntable(self, f):
		
		(head, tail) = path.split(self.fontpath)
		tail = tail[:-4]
		tail += '_kern.ttf'
		fontpath_kern = path.join(head, tail)
		
		tt = ttLib.TTFont(self.fontpath)
		myKernTable = ttLib.newTable('kern')
		myKernSubTable = ttLib.tables._k_e_r_n.KernTable_format_0()
		myKernSubTable.kernTable = {}
		
		cachedKerning = f.kerning
		self.parseKerning(f, cachedKerning.items(), myKernSubTable)

		myKernSubTable.coverage = 1
		myKernSubTable.format = 0
		myKernSubTable.version = 0
		myKernTable.kernTables = [myKernSubTable]
		myKernTable.version = 0

		tt['kern'] = myKernTable
		tt.save(fontpath_kern)
		remove(self.fontpath)
		rename(fontpath_kern, self.fontpath)
		
		
	def parseKerning(self, f, kerningItems, kernSubTable):
		for (pair, value) in kerningItems:
			if self.expandKern == True:
				if pair[0][:1] == '@' and pair[1][:1] == '@':
				#print 'Left and Right are groups'
					for c_keyLeft in f.groups.keys():
						if c_keyLeft == pair[0]:
							#print f.groups[c_keyLeft]
							for gLeftname in f.groups[c_keyLeft]:
								for c_keyRight in f.groups.keys():
									if c_keyRight == pair[1]:
										#print f.groups[c_keyRight]
										for gRightname in f.groups[c_keyRight]:
											processedpair = (gLeftname, gRightname)
											kernSubTable[processedpair] = value
		
				elif pair[1][:1] == '@':
					#print 'Right only is group'
					for c_keyRight in f.groups.keys():
						if c_keyRight == pair[1]:
							#print f.groups[c_keyRight]
							for gname in f.groups[c_keyRight]:
								processedpair = (pair[0], gname)
								kernSubTable[processedpair] = value
		
				elif pair[0][:1] == '@':
					#print 'Left only is group'
					for c_keyLeft in f.groups.keys():
						if c_keyLeft == pair[0]:
							#print f.groups[c_keyLeft]
							for gname in f.groups[c_keyLeft]:
								processedpair = (gname, pair[1])
								kernSubTable[processedpair] = value
						
				else:
					#print 'none is group'
					kernSubTable[pair] = value
					
			else:
			#Do not expand group kerning, just use first item of group
				if pair[0][:1] == '@' and pair[1][:1] == '@':
				#print 'Left and Right are groups'
					for c_keyLeft in f.groups.keys():
						if c_keyLeft == pair[0]:
							#print f.groups[c_keyLeft]
							for c_keyRight in f.groups.keys():
								if c_keyRight == pair[1]:
									#print f.groups[c_keyRight]
									processedpair = (f.groups[c_keyLeft][0], f.groups[c_keyRight][0])
									kernSubTable[processedpair] = value
		
				elif pair[1][:1] == '@':
					#print 'Right only is group'
					for c_keyRight in f.groups.keys():
						if c_keyRight == pair[1]:
							#print f.groups[c_keyRight]
							processedpair = (pair[0], f.groups[c_keyRight][0])
							kernSubTable[processedpair] = value
		
				elif pair[0][:1] == '@':
					#print 'Left only is group'
					for c_keyLeft in f.groups.keys():
						if c_keyLeft == pair[0]:
							#print f.groups[c_keyLeft]
							processedpair = (f.groups[c_keyLeft][0], pair[1])
							kernSubTable[processedpair] = value
						
				else:
					#print 'none is group'
					kernSubTable[pair] = value



f = CurrentFont()
af = AllFonts()
GenerateWindow()