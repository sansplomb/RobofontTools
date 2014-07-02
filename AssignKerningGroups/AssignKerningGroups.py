f = CurrentFont()
kerning = f.kerning
newKerning = {}

def assignGroups(f):
	groupsList = []
	leadersList = []
	for i in f.groups.keys():
		leader = f.groups[i][0]
		leadersList.append(leader)
		groupsList.append(i)
	print len(groupsList)
	print len(leadersList)
	
	for pair, value in kerning.items():
		left = pair[0]
		right = pair[1]
		for i in range(len(leadersList)):
			if left == leadersList[i] and groupsList[i][-5:] != 'RIGHT':
				c_leftKey = groupsList[i]
				for j in range(len(leadersList)):
					if right == leadersList[j] and groupsList[j][-4:] !='LEFT':
						c_rightKey = groupsList[j]
						#print c_leftKey, c_rightKey, value
						newKerning[(c_leftKey, c_rightKey)] = value
			
	f.kerning.clear()
	f.kerning.update(newKerning)

assignGroups(f)
#for pair, value in f.kerning.keys():
#	if pair[0] == '@_LAT_A_UC':
#		print pair, value
		