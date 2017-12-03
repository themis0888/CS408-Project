def read_result():
	tmp = []
	with open('test_result.txt') as f:
		lines = f.readlines()
		tmp = lines
	tmp = [x.strip('\n') for x in tmp]

	result = []
	for i in range(len(tmp)):
		if i%2==1:
			idx = tmp[i].index('_')
			result.append(tmp[i][idx+1:])
		else:
			result.append(tmp[i])
	#print(result)
