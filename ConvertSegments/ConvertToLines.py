			
			
def convertToLine():
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
				if s.selected and s.type == "curve":
					#print 'curve'
					endPoint = c.segments[s_index][2]
					if c.segments[s_index - 1].type == 'curve':
						startPoint = c.segments[s_index - 1][2]
					elif c.segments[s_index - 1].type == 'line':
						startPoint = c.segments[s_index - 1][0]
					#print startPoint, endPoint 
					
					insertAttributes.append([c_index, s_index, (endPoint.x, endPoint.y)])
					
		for i in insertAttributes:
			if i[1] == 0:
				#print 'first segment'
				if g.contours[i[0]][1].type == 'curve':
					#print 'next is curve'
					g.contours[i[0]].insertSegment(i[1], 'line', [i[2]], False)
					g.contours[i[0]][i[1]+1].points[0].x = g.contours[i[0]][i[1] + 2].points[0].x
					g.contours[i[0]][i[1]+1].points[0].y = g.contours[i[0]][i[1] + 2].points[0].y
					g.contours[i[0]].removeSegment(i[1]+1)
				elif g.contours[i[0]][1].type == 'line':
					#print 'next is line'
					g.contours[i[0]].insertSegment(i[1], 'line', [i[2]], False)
					g.contours[i[0]][i[1]+1].points[0].x = g.contours[i[0]][i[1] + 2].points[0].x
					g.contours[i[0]][i[1]+1].points[0].y = g.contours[i[0]][i[1] + 2].points[0].y
					
					g.contours[i[0]][i[1]+1].points[1].x = g.contours[i[0]][i[1] + 2].points[0].x
					g.contours[i[0]][i[1]+1].points[1].y = g.contours[i[0]][i[1] + 2].points[0].y

					g.contours[i[0]].removeSegment(i[1]+1)
			elif i[1] == len(g.contours[i[0]].segments) - 1:
				#print 'last segment'
				if g.contours[i[0]][0].type == 'curve':
					#print 'next is curve'
					g.contours[i[0]].insertSegment(i[1], 'line', [i[2]], False)
					g.contours[i[0]][i[1]+1].points[0].x = g.contours[i[0]][0].points[0].x
					g.contours[i[0]][i[1]+1].points[0].y = g.contours[i[0]][0].points[0].y
					g.contours[i[0]].removeSegment(i[1]+1)
				elif g.contours[i[0]][0].type == 'line':
					#print 'next is line'
					g.contours[i[0]].insertSegment(i[1], 'line', [i[2]], False)
					g.contours[i[0]][i[1]+1].points[0].x = g.contours[i[0]][0].points[0].x
					g.contours[i[0]][i[1]+1].points[0].y = g.contours[i[0]][0].points[0].y
					
					g.contours[i[0]][i[1]+1].points[1].x = g.contours[i[0]][0].points[0].x
					g.contours[i[0]][i[1]+1].points[1].y = g.contours[i[0]][0].points[0].y

					g.contours[i[0]].removeSegment(i[1]+1)
			else:
				if g.contours[i[0]][i[1]+1].type == 'curve':
					#print 'next is curve'
					g.contours[i[0]].insertSegment(i[1], 'line', [i[2]], False)
					g.contours[i[0]][i[1]+1].points[0].x = g.contours[i[0]][i[1] + 2].points[0].x
					g.contours[i[0]][i[1]+1].points[0].y = g.contours[i[0]][i[1] + 2].points[0].y
					g.contours[i[0]].removeSegment(i[1]+1)
				if g.contours[i[0]][i[1]+1].type == 'line':
					#print 'next is line'
					g.contours[i[0]].insertSegment(i[1], 'line', [i[2]], False)
					g.contours[i[0]][i[1]+1].points[0].x = g.contours[i[0]][i[1] + 2].points[0].x
					g.contours[i[0]][i[1]+1].points[0].y = g.contours[i[0]][i[1] + 2].points[0].y
					
					g.contours[i[0]][i[1]+1].points[1].x = g.contours[i[0]][i[1] + 2].points[0].x
					g.contours[i[0]][i[1]+1].points[1].y = g.contours[i[0]][i[1] + 2].points[0].y

					g.contours[i[0]].removeSegment(i[1]+1)
			
		g.update()

				
convertToLine()

