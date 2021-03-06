import sys, random, math, pygame
from pygame.locals import *
from pygame.draw import *
from math import sqrt,cos,sin,atan2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.linestring import LineString
import random

XDIM, YDIM = 600, 600
WINDOW = [XDIM, YDIM]
EPSILON = 10.0
RADIUS = 7
POLY_LIST = []
NODES = []
LINES = []

WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Node:
	x = 0
	y = 0  
	parent = None
	cost = 0 
	def __init__(self, xcoord, ycoord):
		self.x = xcoord
		self.y = ycoord

# add obstacles to the screen | return list of obstacles
def obstacle_crtr(filename, screen):
	with open(filename, "r") as obstacles:
		for line in obstacles:
			x = line.split(" ")
			if len(x) == 1:
				n_corners = int(x[0])
				points = []
				cntr = 0
			else:
				points.append((int(x[0]), int(x[1])))
				POLY_LIST.append(points)
				cntr += 1
				if cntr == n_corners:
					polygon(screen, YELLOW, points, 1)

# add start, goal to screen | return start, goal values
def start_goal(filename, screen):
	with open(filename, "r") as sg:
		s = str.split(sg.readline())
		start = (int(s[0]), int(s[1]))
		circle(screen, GREEN, start, 3, 0)

		g = str.split(sg.readline())
		goal = (int(g[0]), int(g[1]))
		circle(screen, RED, goal, 3, 0)

		return start, goal

# distance formula takes in 2 Nodes
def dist(pt1,pt2):
	return sqrt((pt1.x-pt2.x)*(pt1.x-pt2.x)+(pt1.y-pt2.y)*(pt1.y-pt2.y))

def get_random_pt():
	while True:
		a = int(random.random()*XDIM)
		b = int(random.random()*YDIM)
		p = Point(a,b)
		if collide_pt(p) == False:
			return [a,b]   

def collide_pt(p):
	for poly in POLY_LIST:
		polygoly = Polygon([list(elem) for elem in poly])
		if polygoly.intersects(p):
			return True
	return False

def collide_ln(ln):
	for poly in POLY_LIST:
		polygoly = Polygon([list(elem) for elem in poly])
		for i in range(0, int(ln.length), 5):
			ip = ln.interpolate(i)
			if polygoly.intersects(ip):
				return True
	return False

def lines_cross(ln,min,max):
	for otherln in LINES:
		if ln.crosses(otherln):
			return True
	return False


def find_near_neighbor(pt):
	#print "finding near neighbor"
	nearest = NODES[0]
	ls = LineString([(0,0),(0,0)])
	valid = False
	for n in NODES:
		#print "dist:", dist(n,pt)
		if dist(n,pt) < dist(nearest,pt):
			 nearest = n
	return nearest

def step_to(pt, node):
	longls = LineString([(node.x, node.y),(pt.x, pt.y)])
	ipt = longls.interpolate(30)
	ls = LineString([(ipt.x, ipt.y),(node.x, node.y)])
	if collide_ln(ls) == False and lines_cross(ls,ipt,node) == False and ls.length > 20:
		return ls, ipt, True
	else:
		return ls, ipt, False	

def main():
	#initialize screen with obstacles
	pygame.init()
	screen = pygame.display.set_mode(WINDOW)
	pygame.display.set_caption('HOMEWORK 5 Part 1')
	obstacle_crtr(sys.argv[1], screen)

	start, goal = start_goal(sys.argv[2], screen)
	NODES.append(Node(start[0], start[1]))
	pygame.display.update()

	done = False
	while not done:
		valid = False
		while not valid:
			listpt = get_random_pt()
			pt = Point(listpt[0], listpt[1])
			if collide_pt(pt) == False:
				neighbor_node = find_near_neighbor(pt)
				ls, ipt, valid = step_to(pt, neighbor_node)
		node = Node(ipt.x, ipt.y)
		node.parent = neighbor_node
		NODES.append(node)
		LINES.append(ls)
		circle(screen, GREEN, [int(node.x),int(node.y)], 3, 0)
		line(screen,WHITE,[neighbor_node.x,neighbor_node.y],[node.x,node.y])
		pygame.display.update()

		#checks if point is close enough to goal
		if dist(ipt, Point(goal[0], goal[1])) < 10:
			print "goal reached"
			while True:
				circle(screen, RED, [int(node.x),int(node.y)], 3, 0)
				node = node.parent
				if node is None:
					break
			pygame.display.update()
			done = True
	
	while True:
		pass

if __name__ == '__main__':
	main()