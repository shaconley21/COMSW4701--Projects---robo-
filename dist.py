from math import *

def get_dist(a,b):
	a1 = a[0]
	a2 = a[1]
	b1 = b[0]
	b2 = b[1]
	dist1 = hypot(b1[0] - a1[0], b1[1] - a1[1])
	dist2 = hypot(b2[0] - a2[0], b2[1] - a2[1])
	dist = (dist1+dist2)/2
	return dist
