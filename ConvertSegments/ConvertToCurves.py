def computeInsertAttributes():
	g = CurrentGlyph()
	# SAM SAYS: j'ai viré x_list et y_list car non utilisés
	insertAttributes = []
	for c_index in range(len(g.contours)):
		c = g.contours[c_index]
		for s_index in range(len(c.segments)):
			s = c.segments[s_index]
			#print s.type
			if not s.selected:
			    continue
			if s.type == "line":
				endPoint = s[0]
				prev = c.segments[s_index - 1]
				if prev.type == 'curve':
					startPoint = prev[2]
				elif prev.type in ['line', 'move']:
					startPoint = prev[0]			    
				else: # SAM SAYS: ai ajouté ce warning:
					print("WARNING: I don't know this kind of segment: "+prev.type)        
					continue
				
				third_x = int((endPoint.x - startPoint.x) / 3)
				third_y = int((endPoint.y - startPoint.y) / 3)
				
				insertAttributes.append(
						(	c_index,
							s_index,
							(startPoint.x + third_x, startPoint.y + third_y),
							(endPoint.x   - third_x, endPoint.y   - third_y),
							(endPoint.x, endPoint.y)
						)
					)
	return insertAttributes

def convertToCurve():
	g = CurrentGlyph()
	# SAM SAYS: je test la négation et 'return', ça permet de ne pas avoir à indenter ce qui suit.
	# (compare avec ton test initial)
	if (not g) or g.selection == []:
		return
	g.prepareUndo()
	for i in computeInsertAttributes():
		# SAM SAYS: j'ai changé 'i' en un 'tuple' (en l'occurence, un quintuplet) plutôt qu'une liste,
		# et j'extrais les cinque valeurs d'un coup:
		c_idx, s_idx, p1, p2, p3 = i
		g.contours[c_idx].insertSegment(s_idx, 'curve', (p1, p2, p3), False)
		#print s_idx, len(g.contours[c_idx].segments)
		# SAM SAYS: pas besoin du cas s_idx == 0. Par contre, je pense que ci-dessous, il faut '- 1' et pas '- 2'
		if s_idx == len(g.contours[c_idx].segments) - 2:
			#print 'last segment'
			g.contours[c_idx].removeSegment(0)
		else:
			g.contours[c_idx].removeSegment(s_idx+1)
	g.update()

convertToCurve()
