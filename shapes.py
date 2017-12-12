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

def initialize():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW)
    pygame.display.set_caption('HOMEWORK 5')

    POLY_LIST = obstacle_crtr("world_obstacles.txt", screen)

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
            print "got random point"
            return [a,b]   

def collide_pt(p):
	for poly in POLY_LIST:
        polygoly = Polygon([list(elem) for elem in poly])
        if polygoly.intersects(obj):
            return True
    return False

def collide_ln(ln):
	for poly in POLY_LIST:
		polygoly = Polygon([list(elem) for elem in poly])
		for i in range(0, ln.length, 15):
        	ip = ln.interpolate(i)
        	if polygoly.intersects(ip):
        		print True
        		return True
        		circle(screen, GREEN, [int(ip.x),int(ip.y)], 3, 0)
        	else:
        		print False
        		return False

#TODO
def lines_cross(ln):


def find_near_neighbor(pt):
	print "finding near neighbor"
	nearest = NODES[0]
	valid = False
	for n in NODES:
		#TODO
		if dist(n,pt) < dist(nearest,pt) and dist(n,pt) > 20 and dist(n,pt) < 50:
			ls = LineString([(n.x, n.y),(pt.x, pt.y)])
			if collides_ln(ls) == False and lines_cross(ls) == False:
				nearest = n
				valid = True
	return nearest, ls, valid

def main():
	#initialize screen with obstacles
	initialize()

	start, goal = start_goal("start_goal.txt", screen)
    NODES.append(Node(start[0], start[1]))
    pygame.display.update()

    done = False
    while not done:
    	valid = False
    	while not valid:
	    	listpt = get_random_pt()
	    	pt = Point(listpt[0], listpt[1])
	    	if collide_pt(pt) == False:
	    		neighbor, ls, valid = find_near_neighbor(pt)
	    node = Node(pt.x, pt.y)
	    node.parent = neighbor
	    NODES.append(node)
	    LINES.append(ls)
	    circle(screen, GREEN, listpt, 3, 0)
        line(screen,WHITE,[neighbor.x,neighbor.y],listpt)
        pygame.display.update()

        #checks if point is close enough to goal
        if dist(point, goal) < 50:
        	line(screen,RED,goal,listpt)
            print "goal reached"
            break


if __name__ == '__main__':
    main()