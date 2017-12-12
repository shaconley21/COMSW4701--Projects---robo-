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
EPSILON = 7.0
RADIUS = 7
POLY_LIST = []
NODES = []

WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Node:
    x = 0
    y = 0  
    parent = None
    cost = 0 
    def __init__(self,xcoord, ycoord):
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
        s = sg.readline()
        start = (int(s[0]), int(s[1]))
        circle(screen, GREEN, start, 3, 0)

        g = sg.readline()
        goal = (int(g[0]), int(g[1]))
        circle(screen, GREEN, start, 3, 0)

        return start, goal

# distance formula
def dist(pt1,pt2):
    return sqrt((pt1[0]-pt2[0])*(pt1[0]-pt2[0])+(pt1[1]-pt2[1])*(pt1[1]-pt2[1]))

#"Change up" - Beyonce
# def step_from_to(p1,p2):
#     if dist(p1,p2) < EPSILON:
#         return p2
#     else:
#         theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
#         return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

def get_random_pt():
    while True:
        a = int(random.random()*XDIM)
        b = int(random.random()*YDIM)
        p = Point(a,b)
        if collisions(p) == False:
            return [a,b]   
  
def collisions(obj):
    for poly in POLY_LIST:
        polygoly = Polygon([list(elem) for elem in poly])
        if polygoly.intersects(obj):
            return True
    return False 

def find_near_neighbor(rand):
    nn = NODES[0]
    for p in NODES:
        if dist([p.x,p.y],[rand.x,rand.y]) < dist([nn.x,nn.y],[rand.x,rand.y]) and \
            dist([p.x,p.y],[rand.x,rand.y]) > EPSILON:
            line = LineString([(p.x,p.y), (rand.x,rand.y)])
            if collisions(line) == False:
                nn = p
    return nn

def main():
    #initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINDOW)
    pygame.display.set_caption('HOMEWORK 5')

    POLY_LIST = obstacle_crtr("world_obstacles.txt", screen)
    start, goal = start_goal("start_goal.txt", screen)

    NODES.append(Node(start[0], start[1]))

    pygame.display.update()
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        point = get_random_pt()
        new_node = Point(point[0], point[1])
        collides = collisions(new_node)
        if collides == False:
            near = find_near_neighbor(new_node)
            node = Node(point[0], point[1])
            node.parent = near
            NODES.append(node)
            circle(screen, GREEN, point, 3, 0)
            line(screen,WHITE,[near.x,near.y],point)
            pygame.display.update()
        else:
            print "collided"
        
        # '''
        # newnode = step_from_to
        # NODES.append(newnode)
        # line(screen, WHITE, node, newnode, )

        # if dist(newnode, goal) < EPSILON:
        #     print "goal reached"
        #             break
        # '''
    #pygame.display.update()

if __name__ == '__main__':
    main()


#for finding shortest path, use a graph search algorithm
#aka dijkstra's and co

