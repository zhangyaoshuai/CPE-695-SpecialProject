
def match(lat, long, coor):
	min_lat = coor[0][0][0]
	max_lat = 0
	min_long = coor[0][0][1]
	max_long = 0
	for i in range(len(coor)):
		for j in range(len(coor[i])):
			if coor[i][j][0] >= max_lat:
				max_lat = coor[i][j][0]
			if coor[i][j][1] >= max_long:
				max_long = coor[i][j][1]
			if coor[i][j][0] <= min_lat:
				min_lat = coor[i][j][0]
			if coor[i][j][1] <= min_long:
				min_long = coor[i][j][1]

	if lat <= max_lat and lat >= min_lat and long <= max_long and long >= min_long:
		return True
	else:
		return False



