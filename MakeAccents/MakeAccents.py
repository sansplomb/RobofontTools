from vanilla import *
import math 
from defconAppKit.windows.baseWindow import BaseWindowController

toBeDecomposed = [
				'AE', 'OE', 'Lslash', 'Oslash', 'Eth', 'Thorn',
				'ae', 'oe', 'lslash', 'oslash', 'eth', 'thorn', 'germandbls',
				'ae.sc', 'oe.sc', 'lslash.sc', 'oslash.sc', 'eth.sc', 'thorn.sc',
				'fi', 'fl', 'f_f', 'f_f_i', 'f_f_l', 'f_t', 'f_b', 'f_f_b', 'f_h', 'f_f_h', 'f_k', 'f_f_k', 'f_j', 'f_f_j', 'f_f_t', 'c_t', 's_p', 's_t',
				'Aogonek', 'Ccedilla', 'Eogonek', 'Hbar', 'Iogonek', 'Scedilla', 'Tbar', 'Uogonek',
				'aogonek', 'ccedilla', 'dcroat', 'eogonek', 'hbar', 'iogonek', 'scedilla', 'tbar', 'uogonek',
				'aogonek.sc', 'ccedilla.sc', 'eogonek.sc', 'hbar.sc', 'iogonek.sc', 'scedilla.sc', 'tbar.sc', 'uogonek.sc',
					]
metricsAdjust = [
				'Lcaron', 'Ldot',
				'hcircumflex', 'dcaron', 'lacute', 'lcaron', 'ldot',
				'lcaron.sc', 'ldot.sc',
				]

extrasL = {
		'fi': [['f', 'i'], []],
		'fl': [['f', 'l'], []],
		
		'f_f': [['f', 'f'], []],
		'f_f_i': [['f', 'f', 'i'], []],
		'f_f_l': [['f', 'f', 'l'], []],
		'f_t': [['f', 't'], []],
		'f_b': [['f', 'b'], []],
		'f_f_b': [['f', 'f', 'b'], []],
		'f_h': [['f', 'h'], []],
		'f_f_h': [['f', 'f', 'h'], []],
		'f_k': [['f', 'k'], []],
		'f_f_k': [['f', 'f', 'k'], []],
		'f_j': [['f', 'j'], []],
		'f_f_j': [['f', 'f', 'j'], []],
		'f_f_t': [['f', 'f', 't'], []],
		'c_t': [['c', 't'], []],
		's_p': [['s', 'p'], []],
		's_t': [['s', 't'], []],
		
		
		'AE': [['A', 'E'], []],
		'OE': [['O', 'E'], []], 
		'Lslash': [['L'], ['macron']],
		'Oslash': [['O'], ['slash']],
		'Eth': [['D'], ['macron']],
		'Thorn': [['P'], []],
		
		'Aacute': [['A'], ['acute']], 
		'Acircumflex': [['A'], ['circumflex']],
		'Adieresis': [['A'], ['dieresis']], 
		'Agrave': [['A'], ['grave']],
		'Aring': [['A'], ['ring']],
		'Atilde': [['A'], ['tilde']],
		'Abreve': [['A'], ['breve']],
		'Amacron': [['A'], ['macron']],
		'Aogonek': [['A'], ['ogonek']],
		'Ccedilla': [['C'], ['cedilla']],
		'Cacute': [['C'], ['acute']],
		'Ccaron': [['C'], ['caron']],
		'Ccircumflex': [['C'], ['circumflex']],
		'Cdotaccent': [['C'], ['dotaccent']],
		'Dcaron': [['D'], ['caron']],
		'Dcroat': [['Eth'], []],
		'Eacute': [['E'], ['acute']],
		'Ecircumflex': [['E'], ['circumflex']],
		'Edieresis': [['E'], ['dieresis']],
		'Egrave': [['E'], ['grave']],
		'Ebreve': [['E'], ['breve']],
		'Ecaron': [['E'], ['caron']],
		'Edotaccent': [['E'], ['dotaccent']],
		'Emacron': [['E'], ['macron']],
		'Eogonek': [['E'], ['ogonek']],
		'Gbreve': [['G'], ['breve']],
		'Gcircumflex': [['G'], ['circumflex']],
		'Gcommaaccent': [['G'], ['commaaccent']],
		'Gdotaccent': [['G'], ['dotaccent']],
		'Hbar': [['H'], ['macron']],
		'Hcircumflex': [['H'], ['circumflex']],
		'Iacute': [['I'], ['acute']],
		'Icircumflex': [['I'], ['circumflex']],
		'Idieresis': [['I'], ['dieresis']],
		'Igrave': [['I'], ['grave']],
		'Ibreve': [['I'], ['breve']],
		'Idotaccent': [['I'], ['dotaccent']],
		'Imacron': [['I'], ['macron']],
		'Iogonek': [['I'], ['ogonek']],
		'Itilde': [['I'], ['tilde']],
		'Jcircumflex': [['J'], ['circumflex']],
		'IJ': [['I', 'J'], []],
		'Kcommaaccent': [['K'], ['commaaccent']],
		'Lacute': [['L'], ['acute']], 
		'Lcaron': [['L'], ['caron.alt']],
		'Lcommaaccent': [['L'], ['commaaccent']],
		'Ldot': [['L'], ['periodcentered']],
		'Ntilde': [['N'], ['tilde']],
		'Nacute': [['N'], ['acute']], 
		'Ncaron': [['N'], ['caron']],
		'Ncommaaccent': [['N'], ['commaaccent']],
		'Oacute': [['O'], ['acute']], 
		'Ocircumflex': [['O'], ['circumflex']],
		'Odieresis': [['O'], ['dieresis']],
		'Ograve': [['O'], ['grave']],
		'Otilde': [['O'], ['tilde']],
		'Obreve': [['O'], ['breve']],
		'Ohungarumlaut': [['O'], ['hungarumlaut']],
		'Omacron': [['O'], ['macron']],
		'Racute': [['R'], ['acute']],
		'Rcaron': [['R'], ['caron']], 
		'Rcommaaccent': [['R'], ['commaaccent']],
		'Sacute': [['S'], ['acute']],
		'Scaron': [['S'], ['caron']],
		'Scedilla': [['S'], ['cedilla']], 
		'Scircumflex': [['S'], ['circumflex']], 
		'uni0218': [['S'], ['commaaccent']],
		'Tbar': [['T'], ['macron']],
		'Tcaron': [['T'], ['caron']], 
		'uni0162': [['T'], ['commaaccent']],
		'uni021A': [['T'], ['commaaccent']],
		'Uacute': [['U'], ['acute']],
		'Ucircumflex': [['U'], ['circumflex']],
		'Udieresis': [['U'], ['dieresis']],
		'Ugrave': [['U'], ['grave']],
		'Ubreve': [['U'], ['breve']],
		'Uhungarumlaut': [['U'], ['hungarumlaut']],
		'Umacron': [['U'], ['macron']],
		'Uogonek': [['U'], ['ogonek']],
		'Uring': [['U'], ['ring']],
		'Utilde': [['U'], ['tilde']],
		'Wacute': [['W'], ['acute']],
		'Wcircumflex': [['W'], ['circumflex']],
		'Wdieresis': [['W'], ['dieresis']],
		'Wgrave': [['W'], ['grave']],
		'Yacute': [['Y'], ['acute']],
		'Ycircumflex': [['Y'], ['circumflex']],
		'Ydieresis': [['Y'], ['dieresis']],
		'Ygrave': [['Y'], ['grave']],
		'Zcaron': [['Z'], ['caron']],
		'Zacute': [['Z'], ['acute']],
		'Zdotaccent': [['Z'], ['dotaccent']],
		
		'ae': [['a', 'e'], []], 
		'oe': [['o', 'e'], []], 
		'lslash': [['l'], ['macron']],
		'oslash': [['o'], ['slash']],
		'eth': [['d'], ['macron']],
		'thorn': [['p'], []],
		'germandbls': [['f', 's'], []],
		
		'aacute': [['a'], ['acute']], 
		'acircumflex': [['a'], ['circumflex']],
		'adieresis': [['a'], ['dieresis']], 
		'agrave': [['a'], ['grave']],
		'aring': [['a'], ['ring']],
		'atilde': [['a'], ['tilde']],
		'abreve': [['a'], ['breve']],
		'amacron': [['a'], ['macron']],
		'aogonek': [['a'], ['ogonek']],
		'ccedilla': [['c'], ['cedilla']],
		'cacute': [['c'], ['acute']],
		'ccaron': [['c'], ['caron']],
		'ccircumflex': [['c'], ['circumflex']],
		'cdotaccent': [['c'], ['dotaccent']],
		'dcaron': [['d'], ['caron.alt']],
		'dcroat': [['d'], ['macron']],
		'eacute': [['e'], ['acute']],
		'ecircumflex': [['e'], ['circumflex']],
		'edieresis': [['e'], ['dieresis']],
		'egrave': [['e'], ['grave']],
		'ebreve': [['e'], ['breve']],
		'ecaron': [['e'], ['caron']],
		'edotaccent': [['e'], ['dotaccent']],
		'emacron': [['e'], ['macron']],
		'eogonek': [['e'], ['ogonek']],
		'gbreve': [['g'], ['breve']],
		'gcircumflex': [['g'], ['circumflex']],
		'gcommaaccent': [['g'], ['revcommaaccent']],
		'gdotaccent': [['g'], ['dotaccent']],
		'hbar': [['h'], ['macron']],
		'hcircumflex': [['h'], ['circumflex']],
		'iacute': [['dotlessi'], ['acute']],
		'icircumflex': [['dotlessi'], ['circumflex']],
		'idieresis': [['dotlessi'], ['dieresis']],
		'igrave': [['dotlessi'], ['grave']],
		'ibreve': [['dotlessi'], ['breve']],
		'i.dot': [['i'], []],
		'imacron': [['dotlessi'], ['macron']],
		'iogonek': [['dotlessi'], ['ogonek']],
		'itilde': [['dotlessi'], ['tilde']],
		'jcircumflex': [['dotlessj'], ['circumflex']],
		'ij': [['i', 'j'], []],
		'kcommaaccent': [['k'], ['commaaccent']],
		'lacute': [['l'], ['acute']], 
		'lcaron': [['l'], ['caron.alt']],
		'lcommaaccent': [['l'], ['commaaccent']],
		'ldot': [['l'], ['periodcentered']],
		'ntilde': [['n'], ['tilde']],
		'nacute': [['n'], ['acute']], 
		'ncaron': [['n'], ['caron']],
		'ncommaaccent': [['n'], ['commaaccent']],
		'oacute': [['o'], ['acute']], 
		'ocircumflex': [['o'], ['circumflex']],
		'odieresis': [['o'], ['dieresis']],
		'ograve': [['o'], ['grave']],
		'otilde': [['o'], ['tilde']],
		'obreve': [['o'], ['breve']],
		'ohungarumlaut': [['o'], ['hungarumlaut']],
		'omacron': [['o'], ['macron']],
		'racute': [['r'], ['acute']],
		'rcaron': [['r'], ['caron']], 
		'rcommaaccent': [['r'], ['commaaccent']],
		'sacute': [['s'], ['acute']],
		'scaron': [['s'], ['caron']],
		'scedilla': [['s'], ['cedilla']], 
		'scircumflex': [['s'], ['circumflex']], 
		'uni0219': [['s'], ['commaaccent']],
		'tbar': [['t'], ['macron']],
		'tcaron': [['t'], ['caron.alt']], 
		'uni0163': [['t'], ['commaaccent']],
		'uni021B': [['t'], ['commaaccent']],
		'uacute': [['u'], ['acute']],
		'ucircumflex': [['u'], ['circumflex']],
		'udieresis': [['u'], ['dieresis']],
		'ugrave': [['u'], ['grave']],
		'ubreve': [['u'], ['breve']],
		'uhungarumlaut': [['u'], ['hungarumlaut']],
		'umacron': [['u'], ['macron']],
		'uogonek': [['u'], ['ogonek']],
		'uring': [['u'], ['ring']],
		'utilde': [['u'], ['tilde']],
		'wacute': [['w'], ['acute']],
		'wcircumflex': [['w'], ['circumflex']],
		'wdieresis': [['w'], ['dieresis']],
		'wgrave': [['w'], ['grave']],
		'yacute': [['y'], ['acute']],
		'ycircumflex': [['y'], ['circumflex']],
		'ydieresis': [['y'], ['dieresis']],
		'ygrave': [['y'], ['grave']],
		'zcaron': [['z'], ['caron']],
		'zacute': [['z'], ['acute']],
		'zdotaccent': [['z'], ['dotaccent']],
		
		'ae.sc': [['a.sc', 'e.sc'], []], 
		'oe.sc': [['o.sc', 'e.sc'], []], 
		'lslash.sc': [['l.sc'], ['macron']],
		'oslash.sc': [['o.sc'], ['slash']],
		'eth.sc': [['d.sc'], ['macron']],
		'thorn.sc': [['p.sc'], []],
		'germandbls.sc': [['s.sc', 's.sc'], []],
		'dotlessi.sc': [['i.sc'], []],
		'dotlessj.sc': [['j.sc'], []],
		
		'aacute.sc': [['a.sc'], ['acute']], 
		'acircumflex.sc': [['a.sc'], ['circumflex']],
		'adieresis.sc': [['a.sc'], ['dieresis']], 
		'agrave.sc': [['a.sc'], ['grave']],
		'aring.sc': [['a.sc'], ['ring']],
		'atilde.sc': [['a.sc'], ['tilde']],
		'abreve.sc': [['a.sc'], ['breve']],
		'amacron.sc': [['a.sc'], ['macron']],
		'aogonek.sc': [['a.sc'], ['ogonek']],
		'ccedilla.sc': [['c.sc'], ['cedilla']],
		'cacute.sc': [['c.sc'], ['acute']],
		'ccaron.sc': [['c.sc'], ['caron']],
		'ccircumflex.sc': [['c.sc'], ['circumflex']],
		'cdotaccent.sc': [['c.sc'], ['dotaccent']],
		'dcaron.sc': [['d.sc'], ['caron']],
		'dcroat.sc': [['eth.sc'], []],
		'eacute.sc': [['e.sc'], ['acute']],
		'ecircumflex.sc': [['e.sc'], ['circumflex']],
		'edieresis.sc': [['e.sc'], ['dieresis']],
		'egrave.sc': [['e.sc'], ['grave']],
		'ebreve.sc': [['e.sc'], ['breve']],
		'ecaron.sc': [['e.sc'], ['caron']],
		'edotaccent.sc': [['e.sc'], ['dotaccent']],
		'emacron.sc': [['e.sc'], ['macron']],
		'eogonek.sc': [['e.sc'], ['ogonek']],
		'gbreve.sc': [['g.sc'], ['breve']],
		'gcircumflex.sc': [['g.sc'], ['circumflex']],
		'gcommaaccent.sc': [['g.sc'], ['commaaccent']],
		'gdotaccent.sc': [['g.sc'], ['dotaccent']],
		'hbar.sc': [['h.sc'], ['macron']],
		'hcircumflex.sc': [['h.sc'], ['circumflex']],
		'iacute.sc': [['i.sc'], ['acute']],
		'icircumflex.sc': [['i.sc'], ['circumflex']],
		'idieresis.sc': [['i.sc'], ['dieresis']],
		'igrave.sc': [['i.sc'], ['grave']],
		'ibreve.sc': [['i.sc'], ['breve']],
		'i.dot.sc': [['i.sc'], ['dotaccent']],
		'imacron.sc': [['i.sc'], ['macron']],
		'iogonek.sc': [['i.sc'], ['ogonek']],
		'itilde.sc': [['i.sc'], ['tilde']],
		'jcircumflex.sc': [['j.sc'], ['circumflex']],
		'ij.sc': [['i.sc', 'j.sc'], []],
		'kcommaaccent.sc': [['k.sc'], ['commaaccent']],
		'lacute.sc': [['l.sc'], ['acute']], 
		'lcaron.sc': [['l.sc'], ['caron.alt']],
		'lcommaaccent.sc': [['l.sc'], ['commaaccent']],
		'ldot.sc': [['l.sc'], ['periodcentered']],
		'ntilde.sc': [['n.sc'], ['tilde']],
		'nacute.sc': [['n.sc'], ['acute']], 
		'ncaron.sc': [['n.sc'], ['caron']],
		'ncommaaccent.sc': [['n.sc'], ['commaaccent']],
		'oacute.sc': [['o.sc'], ['acute']], 
		'ocircumflex.sc': [['o.sc'], ['circumflex']],
		'odieresis.sc': [['o.sc'], ['dieresis']],
		'ograve.sc': [['o.sc'], ['grave']],
		'otilde.sc': [['o.sc'], ['tilde']],
		'obreve.sc': [['o.sc'], ['breve']],
		'ohungarumlaut.sc': [['o.sc'], ['hungarumlaut']],
		'omacron.sc': [['o.sc'], ['macron']],
		'racute.sc': [['r.sc'], ['acute']],
		'rcaron.sc': [['r.sc'], ['caron']], 
		'rcommaaccent.sc': [['r.sc'], ['commaaccent']],
		'sacute.sc': [['s.sc'], ['acute']],
		'scaron.sc': [['s.sc'], ['caron']],
		'scedilla.sc': [['s.sc'], ['cedilla']], 
		'scircumflex.sc': [['s.sc'], ['circumflex']], 
		'uni0219.sc': [['s.sc'], ['commaaccent']],
		'tbar.sc': [['t.sc'], ['macron']],
		'tcaron.sc': [['t.sc'], ['caron']], 
		'uni0163.sc': [['t.sc'], ['commaaccent']],
		'uni021B.sc': [['t.sc'], ['commaaccent']],
		'uacute.sc': [['u.sc'], ['acute']],
		'ucircumflex.sc': [['u.sc'], ['circumflex']],
		'udieresis.sc': [['u.sc'], ['dieresis']],
		'ugrave.sc': [['u.sc'], ['grave']],
		'ubreve.sc': [['u.sc'], ['breve']],
		'uhungarumlaut.sc': [['u.sc'], ['hungarumlaut']],
		'umacron.sc': [['u.sc'], ['macron']],
		'uogonek.sc': [['u.sc'], ['ogonek']],
		'uring.sc': [['u.sc'], ['ring']],
		'utilde.sc': [['u.sc'], ['tilde']],
		'wacute.sc': [['w.sc'], ['acute']],
		'wcircumflex.sc': [['w.sc'], ['circumflex']],
		'wdieresis.sc': [['w.sc'], ['dieresis']],
		'wgrave.sc': [['w.sc'], ['grave']],
		'yacute.sc': [['y.sc'], ['acute']],
		'ycircumflex.sc': [['y.sc'], ['circumflex']],
		'ydieresis.sc': [['y.sc'], ['dieresis']],
		'ygrave.sc': [['y.sc'], ['grave']],
		'zcaron.sc': [['z.sc'], ['caron']],
		'zacute.sc': [['z.sc'], ['acute']],
		'zdotaccent.sc': [['z.sc'], ['dotaccent']]
			}
			
class Process(BaseWindowController):

	def __init__(self):
		self.w = FloatingWindow((200, 55))
		#self.w.bar = ProgressBar((10, 10, -10, 16), sizeStyle = "small")
		self.w.textBox = TextBox((10, 10, -10, 16), "Diacritics", sizeStyle = "regular", alignment = "center")
		self.w.buttonMake = Button((10, -20, 90, 15), "Make", sizeStyle = "small", callback=self.showProgress)
		self.w.buttonDelete = Button((110, -20, -10, 15), "Delete", sizeStyle = "small", callback=self.showDelete)
		self.w.center()
		self.w.open()
		
	
	def showProgress(self, sender):
		self.progress = self.startProgress("Checking UFO...", tickCount=100)
		glyphsToMake = self.defineGlyphsToMake(f, extrasL)
		self.progress.close()
		self.progress = self.startProgress("Processing...", tickCount=100)
		self.makeGlyphs(f, glyphsToMake)
		self.progress.close()
		self.w.close()
	
	def showDelete(self, sender):
		self.progress = self.startProgress("Deleting Diactitics...", tickCount=100)
		self.deleteAll(f)
		self.progress.close()
		
	def deleteAll(self, f):
		self.progress.setTickCount(len(extrasL.keys()))
		for i in extrasL.keys():
			self.progress.update()
			if i in f.keys():
				f.removeGlyph(i)

	def defineGlyphsToMake(self, f, extrasDict):
		glyphsToMake = {}
		self.progress.setTickCount(len(extrasDict.keys()))
		for i in extrasDict.keys():
			self.progress.update()
			newGlyphName = i
			basesNames = extrasDict[i][0]
			accentsNames = extrasDict[i][1]
			missing = False
			#print newGlyphName, basesNames, accentsNames
			if i in f.keys():
				continue
				#print 'glyph ' + i + ' already exists'
			else:
				#check if components are present in the font
				for base in basesNames:
					if len(accentsNames) > 0:
						for accent in accentsNames:
							if base in f.keys() and accent in f.keys():
								continue
							elif base not in f.keys():
								#print 'glyph ' + base + ' is missing'
								#missingBases.append(base)
								missing = True
							elif accent not in f.keys():
								#print 'glyph ' + accent + ' is missing'
								#missingAccents.append(accent)
								missing = True
					else:
						if base not in f.keys():
							#print 'glyph ' + base + ' is missing'
							missing = True
				if missing == False:
					#print 'glyph ' + i + ' to create'
					glyphsToMake[i] = (basesNames , accentsNames)

		return glyphsToMake

	def makeGlyphs(self, f, glyphsToMake):	
		self.progress.setTickCount(len(glyphsToMake.keys()))
		for i in glyphsToMake.keys():
			self.progress.update()
			basesNames = glyphsToMake[i][0] 
			accentsNames = glyphsToMake[i][1] 
			f.newGlyph(i)
			markColor = (0, 1, 1, 0.5)
			if i in toBeDecomposed:
				markColor = (0, 1, 0, 0.5)
			elif i in metricsAdjust:
				markColor = (0, 0, 1, 0.5)
			f[i].mark = markColor
			f[i].width = 0
			yShift = 0
			xShift = 0
			for base in basesNames:
				if base.isupper():
					yShift = yShiftCaps
					xShift = xShiftCaps
				if base[-2:] == 'sc':
					yShift = yShiftSmallCaps
					xShift = xShiftSmallCaps
				f[i].appendComponent(base, (f[i].width, 0))
				f[i].width += f[base].width
			for accent in accentsNames:
				if accent == 'ogonek' or accent == 'cedilla' or accent == 'slash' or accent == 'commaaccent' or accent == 'caron.alt' or accent == 'periodcentered':
					yShift = 0
				f[i].appendComponent(accent, ((f[i].width/2 - f[accent].width/2)+xShift, yShift))
			f[i].update()
			
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
glyphsToMake = {}
missingBases = []
missingAccents = []

if 'O' in f.keys() and 'o' in f.keys():
	yShiftCaps = f['O'].box[3] - f['o'].box[3]
else:
	yShiftCaps = 0
if 'o' in f.keys() and 'o.sc' in f.keys():
	yShiftSmallCaps = f['o.sc'].box[3] - f['o'].box[3]
else:
	yShiftSmallCaps = 0
italAngle = getItalAngle(f)
italRatio = getItalRatio(italAngle)
xShiftCaps = getxShift(yShiftCaps, italRatio)
xShiftSmallCaps = getxShift(yShiftSmallCaps, italRatio)

Process()
f.update()
