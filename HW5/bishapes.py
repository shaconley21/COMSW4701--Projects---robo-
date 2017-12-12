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
SNODES = []
GNODES = []
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
				circle(screen, GREEN, [int(ip.x),int(ip.y)], 3, 0)
	return False

def lines_cross(ln,min,max,screen):
	for otherln in LINES:
		if ln.crosses(otherln):
			return True
	return False


def sfind_near_neighbor(pt, screen):
	#print "finding near neighbor"
	nearest = SNODES[0]
	ls = LineString([(0,0),(0,0)])
	valid = False
	for n in SNODES:
		#print "dist:", dist(n,pt)
		if dist(n,pt) < dist(nearest,pt):
			 nearest = n
	return nearest

def gfind_near_neighbor(pt, screen):
	#print "finding near neighbor"
	nearest = GNODES[0]
	ls = LineString([(0,0),(0,0)])
	valid = False
	for n in GNODES:
		#print "dist:", dist(n,pt)
		if dist(n,pt) < dist(nearest,pt):
			 nearest = n
	return nearest	

def step_to(pt, node, screen):
	longls = LineString([(node.x, node.y),(pt.x, pt.y)])
	ipt = longls.interpolate(30)
	ls = LineString([(ipt.x, ipt.y),(node.x, node.y)])
	if collide_ln(ls) == False and lines_cross(ls,ipt,node,screen) == False and ls.length > 20:
		circle(screen, YELLOW, [int(ipt.x), int(ipt.y)], 3, 0)
		return ls, ipt, True
	else:
		return ls, ipt, False	

def main():
	#initialize screen with obstacles
	pygame.init()
	screen = pygame.display.set_mode(WINDOW)
	pygame.display.set_caption('HOMEWORK 5 Part 2')
	obstacle_crtr(sys.argv[1], screen)

	start, goal = start_goal(sys.argv[2], screen)
	SNODES.append(Node(start[0], start[1]))
	GNODES.append(Node(goal[0], goal[1]))
	pygame.display.update()

	done = False
	while not done:
		valid = False
		while not valid:
			listpt = get_random_pt()
			pt = Point(listpt[0], listpt[1])
			if collide_pt(pt) == False:
				neighbor_node = sfind_near_neighbor(pt, screen)
				ls, ipt, valid = step_to(pt, neighbor_node, screen)
		node = Node(ipt.x, ipt.y)
		node.parent = neighbor_node
		SNODES.append(node)
		LINES.append(ls)
		circle(screen, GREEN, [int(node.x),int(node.y)], 3, 0)
		line(screen,GREEN,[neighbor_node.x,neighbor_node.y],[node.x,node.y])
		pygame.display.update()

		for n in GNODES:
			if dist(node, n) < 30:
				lnstr = LineString([(node.x, node.y),(n.x, n.y)])
				if collide_ln(lnstr) == False:
					print "trees merged"
					line(screen,YELLOW,[n.x,n.y],[node.x,node.y])
					pygame.display.update()
					done = True
					break

		valid = False
		while not valid:
			listpt = get_random_pt()
			pt = Point(listpt[0], listpt[1])
			if collide_pt(pt) == False:
				neighbor_node = gfind_near_neighbor(pt, screen)
				ls, ipt, valid = step_to(pt, neighbor_node, screen)
		node = Node(ipt.x, ipt.y)
		node.parent = neighbor_node
		GNODES.append(node)
		LINES.append(ls)
		circle(screen, RED, [int(node.x),int(node.y)], 3, 0)
		line(screen,RED,[neighbor_node.x,neighbor_node.y],[node.x,node.y])
		pygame.display.update()

		for n in SNODES:
			if dist(node, n) < 30:
				lnstr = LineString([(node.x, node.y),(n.x, n.y)])
				if collide_ln(lnstr) == False:
					print "trees merged"
					line(screen,YELLOW,[n.x,n.y],[node.x,node.y])
					pygame.display.update()
					done = True
					break


	while True:
		pass

if __name__ == '__main__':
	main()