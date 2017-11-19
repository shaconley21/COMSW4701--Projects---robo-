from math import atan

def angle_finder(a1, a2, b1, b2):
	a_slope = float((a2[1]-a1[1])/(a2[0]-a1[0]))
	b_slope = float((b2[1]-b1[1])/(b2[0]-b1[0]))
	angle = atan(float((a_slope-b_slope)/(1+a_slope*b_slope)))
	if angle == 90:
		return True
	else:
		return False