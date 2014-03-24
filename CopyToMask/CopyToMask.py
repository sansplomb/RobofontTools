
g = CurrentGlyph()

mask = g.getLayer("mask")
mask.prepareUndo()
g.prepareUndo()

mask.clear()
g.copyToLayer("mask")
mask.update()

g.update()		
