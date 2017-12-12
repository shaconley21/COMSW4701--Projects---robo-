import sys, random, math, pygame
from pygame.locals import *
from pygame.draw import *
from math import sqrt,cos,sin,atan2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import random

X, Y = 600, 600
WINDOW = [X, Y]
EPSILON = 7.0
RADIUS = 7
NUM_NODES = 3000 


class Node:
    x = 0
    y = 0  
    parent = None
    cost = 0 
    def __init__(self,xcoord, ycoord):
         self.x = xcoord
         self.y = ycoord

# need to make a fuction to check intersection that takes three arguments 

def reconnect(nodes,newnode,pygame,screen):
        white = 255, 240, 200
        black = 20, 20, 40
        for i in range(len(nodes)):
           p = nodes[i]
           # if check intersection for p,newnode,OBS and p!=newnode.parent and dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < p.cost:
              pygame.draw.line(screen,white,[p.x,p.y],[p.parent.x,p.parent.y])  
              p.parent = newnode
              p.cost=newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y]) 
              nodes[i]=p  
              pygame.draw.line(screen,black,[p.x,p.y],[newnode.x,newnode.y])                    
        return nodes

def drawSolutionPath(start,goal,nodes,pygame,screen):
    pink = 200, 20, 240
    nn = nodes[0]
    for p in nodes:
       if dist([p.x,p.y],[goal.x,goal.y]) < dist([nn.x,nn.y],[goal.x,goal.y]):
          nn = p
    while nn!=start:
        pygame.draw.line(screen,pink,[nn.x,nn.y],[nn.parent.x,nn.parent.y],5)  
        nn=nn.parent


def select_Parent(nn,newnode,nodes):
        for p in nodes:
         if #check the intersection of p, newnode, and obstacle and dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and p.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y]):
          nn = p
        newnode.cost=nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y])
        newnode.parent=nn
        return newnode,nn

# add obstacles to the screen | return list of obstacles
def obstacle_crtr(filename, screen):
    yellow = (255, 215, 0)
    poly_list = []
    with open(filename, "r") as obstacles:
        for line in obstacles:
            x = line.split(" ")
            if len(x) == 1:
                n_corners = int(x[0])
                points = []
                cntr = 0
            else:
                points.append((int(x[0]), int(x[1])))
                poly_list.append(Polygon(points))
                cntr += 1
                if cntr == n_corners:
                    polygon(screen, yellow, points, 1)
    return poly_list

# add start, goal to screen | return start, goal values
def start_goal(filename, screen):
    green = (0, 255, 0)
    red = (255, 0, 0)
    with open(filename, "r") as sg:
        s = sg.readline()
        start = (int(s[0]), int(s[1]))
        circle(screen, green, start, 3, 0)

        g = sg.readline()
        goal = (int(g[0]), int(g[1]))
        circle(screen, green, start, 3, 0)

        return start, goal

# distance formula
def dist(pt1,pt2):
    return sqrt((pt1[0]-pt2[0])*(pt1[0]-pt2[0])+(pt1[1]-pt2[1])*(pt1[1]-pt2[1]))

#"Change up" - Beyonce
def step_from_to(p1,p2):
    if dist(p1,p2) < EPSILON:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

def get_random_pt():
    while True:
        p = random.random()*X, random.random()*Y
        if collisions(p) == False:
            return p      
          
def collisions(poly_list, point):
    pt = Point(point[0], point[1])
    for poly in poly_list:
        if poly.contains(pt):
            return True
    return False 

def main():
    #initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINDOW)
    pygame.display.set_caption('HOMEWORK 5')

    poly_list = obstacle_crtr("world_obstacles.txt", screen)
    start, goal = start_goal("start_goal.txt", screen)

    nodes = []
    nodes.append(start)
    start = node[0]
    goal = Node(600, 480)
    for i in range(NUM_NODES):
        rand = get_random_pt()
        nn = nodes[0]
        for p in nodes:
            if dist([p.x,p.y],[rand.x,rand.y]) < dist([nn.x,nn.y],[rand.x,rand.y]):
                nn = p
        
        interpolated_node = step_from_to([nn.x,nn.y],[rand.x,rand.y]
        newnode = Node(interpolatedNode[0],interpolatedNode[1])
        # add some condition checking the intersection between nn, rand, and obstacle 
            [newnode,nn]=select_Parent(nn,newnode,nodes);
            nodes.append(newnode)
    pygame.draw.line(screen,black,[nn.x,nn.y],[newnode.x,newnode.y])
    nodes=reconnect(nodes,newnode,pygame,screen)
    pygame.display.update()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        '''
        newnode = step_from_to
        nodes.append(newnode)
        line(screen, white, node, newnode, )

        if dist(newnode, goal) < EPSILON:
            print "goal reached"
                    break
        '''
        pygame.display.update()

if __name__ == '__main__':
    main()


#for finding shortest path, use a graph search algorithm
#aka dijkstra's and co

