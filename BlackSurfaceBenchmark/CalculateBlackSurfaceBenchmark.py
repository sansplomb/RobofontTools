import freetype
import os
import time


f = CurrentFont()
g = CurrentGlyph()

def calculateBlackRaster(g):
	if g == None:
		print 'selcet a glyph first'
		return
	
	root =  os.path.split(f.path)[0]
	tail = 'Temp.ttf'
	fulltempfontpath = os.path.join(root, tail)

	f.generate(fulltempfontpath,'ttf', decompose = False, checkOutlines = False, autohint = False, releaseMode = False, glyphOrder=None, progressBar = None )
	
	start = time.time()
	
	face = freetype.Face(fulltempfontpath)
	face.set_pixel_sizes(1000, 1000)
	face.load_char(g.name, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO )

	surface = len(face.glyph.bitmap.buffer)
	black = 0
	for pixel in face.glyph.bitmap.buffer:
		if pixel == 255:
			black += 1
			
	print "with FreeType:"
	print "finished in %f seconds" % (time.time() - start)
	print 'black:', (black/surface)*100, '%'
	
def calculateBlackContains(g):
	if g == None:
		print 'selcet a glyph first'
		return
	path = g.naked().getRepresentation("defconAppKit.NSBezierPath")
	xMin, yMin, xMax, yMax = g.box
	xMin = int(round(xMin))
	yMin = int(round(yMin))
	xMax= int(round(xMax))
	yMax = int(round(yMax))
	surface = (xMax - xMin) * (yMax - yMin)

	start = time.time()
	black = 0
	for x in range(xMin, xMax):
		for y in range(yMin, yMax):
			if path.containsPoint_((x,y)):
				black += 1

	print "with containsPoint:"
	print "finished in %f seconds" % (time.time() - start)
	print 'black:', (black/surface)*100, '%'
	
calculateBlackRaster(g)
calculateBlackContains(g)