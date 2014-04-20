import os

f = CurrentFont()

currentpath = f.path
root, tail =  os.path.split(f.path)
QuadraticFontTail = 'Quatratic_' + tail.split('.')[0] + '.ttf'
QuadraticUFOTail = 'Quatratic_' + tail.split('.')[0] + '.ufo'
QuadraticFontpath = os.path.join(root, QuadraticFontTail)
QuadraticUFOPath = os.path.join(root, QuadraticUFOTail)

f.generate(QuadraticFontpath, 'ttf', decompose = False, checkOutlines = False, autohint = False, releaseMode = False, glyphOrder=None, progressBar = None )

quadraticFont = OpenFont(QuadraticFontpath, showUI=False)
quadraticFont.save(QuadraticUFOPath)

os.remove(QuadraticFontpath)
f.close()
OpenFont(QuadraticUFOPath, showUI=True)