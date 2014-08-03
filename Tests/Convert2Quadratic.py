from lib.tools.bezierTools import curveConverter
import copyFontInfos as CFI
import os
reload(CFI)

def Convert2Quadratic(f, RemoveOverlap=False):
	currentpath = f.path
	root, tail =  os.path.split(f.path)
	QuadraticUFOTail = 'Quatratic_' + tail.split('.')[0] + '.ufo'
	QuadraticUFOPath = os.path.join(root, QuadraticUFOTail)
	
	nf = NewFont()
	nf.preferredSegmentType = "qCurve"
	CFI.copyAllInfoFromTo(f, nf)
	for g in f:
		nf[g.name] = g.copy()
	for g in nf:
		if RemoveOverlap:
			g.removeOverlap()
		mask = g.getLayer("CubicContour")
		mask.clear()
		g.copyToLayer("CubicContour")
		glyphNaked = g.naked()
		
		if curveConverter.isBezier(glyphNaked):
			curveConverter.bezier2quadratic(glyphNaked)
			glyphNaked.correctDirection(trueType=True)
			
	nf.save(QuadraticUFOPath)
			
f = CurrentFont()
Convert2Quadratic(f, True)