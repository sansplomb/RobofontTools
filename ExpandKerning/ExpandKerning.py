f = CurrentFont()
cachedKerning = f.kerning

	#print pair, value
def expandKerning(kerningItems):
	expandedKerning = {}
	for (pair, value) in kerningItems:
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
									expandedKerning[processedpair] = value
		
		elif pair[1][:1] == '@':
			#print 'Right only is group'
			for c_keyRight in f.groups.keys():
				if c_keyRight == pair[1]:
					#print f.groups[c_keyRight]
					for gname in f.groups[c_keyRight]:
						processedpair = (pair[0], gname)
						expandedKerning[processedpair] = value
		
		elif pair[0][:1] == '@':
			#print 'Left only is group'
			for c_keyLeft in f.groups.keys():
				if c_keyLeft == pair[0]:
					#print f.groups[c_keyLeft]
					for gname in f.groups[c_keyLeft]:
						processedpair = (gname, pair[1])
						expandedKerning[processedpair] = value
						
		else:
			#print 'none is group'
			expandedKerning[pair] = value
			
	return expandedKerning

print 'expanding kerning...'
myexpandedKerning = expandKerning(cachedKerning.items())
print 'updating kerning...'	
f.kerning.update(myexpandedKerning)
print 'clearing groups...'	
f.groups.clear()
print 'DONE'