		
def convertToCurve():
	g = CurrentGlyph()	
	if g and g.selection != []:
		g.prepareUndo()
		a_list_x = []
		a_list_y = []
		insertAttributes = []
		
		for c_index in range(len(g.contours)):
			c = g.contours[c_index]
			for s_index in range(len(c.segments)):
				s = c.segments[s_index]
				if s.selected and s.type == "line":
					endPoint = s[0]
					if c.segments[s_index - 1].type == 'curve':
						startPoint = c.segments[s_index - 1][2]
					elif c.segments[s_index - 1].type == 'line':
						startPoint = c.segments[s_index - 1][0]
					#startPoint = c.segments[s_index - 1][0]
					#print startPoint, endPoint 
					
					a_list_x = [startPoint.x, endPoint.x]
					a_list_y = [startPoint.y, endPoint.y]
					third_x = int((endPoint.x - startPoint.x) / 3)
					third_y = int((endPoint.y - startPoint.y) / 3)
					
					insertAttributes.append([c_index, s_index, (startPoint.x + third_x, startPoint.y + third_y), (endPoint.x - third_x, endPoint.y - third_y), (endPoint.x, endPoint.y)])
					
		for i in insertAttributes:
			g.contours[i[0]].insertSegment(i[1], 'curve', (i[2], i[3], i[4]), False)
			#print i[1], len(g.contours[i[0]].segments)
			if i[1] == 0:
				#print 'first segment'
				g.contours[i[0]].removeSegment(1)
			elif i[1] == len(g.contours[i[0]].segments) - 2:
				#print 'last segment'
				g.contours[i[0]].removeSegment(0)
			else:
				g.contours[i[0]].removeSegment(i[1]+1)
		g.update()

convertToCurve()