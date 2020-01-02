import math
from math import atan2, degrees, pi
import random
import pygame
import random
import os
import neat
import tkinter as tk
from tkinter import messagebox

width = 100
height = 100

rows = 10


class cube():
    rows = 10
    w = 100
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)


    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)



class snake():
    body = []
    turns = {}

    def __init__(self, color, pos):
        #pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.obs_left = 0
        self.obs_right = 0
        self.obs_top = 0
        self.obs_bot = 0

    def move(self, key):
        if key == 0:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        elif key == 1:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        elif key == 2:
            self.dirny = -1
            self.dirnx = 0
            self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        elif key == 3:
            self.dirny = 1
            self.dirnx = 0
            self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)


    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



def redrawWindow():
    global win
    win.fill((0,0,0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue
        else:
               break

    return (x,y)

def get_angle(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p2[1]
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads) / 180
    return degs

def obstacles(s):
    headPos = s.head.pos
    if headPos[0] >= 20:
        s.obs_right = 1
    if headPos[0] < 0:
        s.obs_left = 1
    if headPos[1] >= 20:
        s.obs_top = 1
    if headPos[1] < 0:
        s.obs_bot = 1

    return s.obs_left, s.obs_right, s.obs_top, s.obs_bot

def main(genomes, config):
    global s, snack, win
    win = pygame.display.set_mode((width,height))
    #s = snake((255,0,0), (10,10))
    #s.addCube()
    #snack = cube(randomSnack(rows,s), color=(0,255,0))
    flag = True
    clock = pygame.time.Clock()

    snakes, nets, ge, ids, foods = [], [], [], [], []
    actions = [0, 1, 2, 3]

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        s = snake((255,0,0), (5,5))
        snakes.append(s)
        snack = cube(randomSnack(rows, s), color=(0,255,0))
        foods.append(snack)
        g.fitness = 0
        ge.append(g)
        ids.append(id)

        while flag:
            pygame.time.delay(50)
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            headPos = s.head.pos
            angle_to_food = get_angle(headPos, snack.pos)
            s.obs_left, s.obs_right, s.obs_top, s.obs_bot = obstacles(s)
            random_action = random.choice(actions)
            #s.move(random_action)
            g.fitness -= 1
            output = net.activate((s.obs_left, s.obs_right, s.obs_top, s.obs_bot,
                                        angle_to_food))
            if output[0] < 0:
                s.move(0)
            elif output[0] > 0.5:
                s.move(1)
            else:
                s.move(2)

            if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
                g.fitness -= 1
                break
                #print("Score:", len(s.body))
                #s.reset((10, 10))

            if headPos == snack.pos:
                s.addCube()
                snack = cube(randomSnack(rows,s), color=(0,255,0))
                g.fitness += 5

            redrawWindow()

def run(config_file):
    ## Read the config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)

    ## Generate a population based on the config file
    population = neat.Population(config)
    ## Optional Stats within the console
    stats = neat.StatisticsReporter()
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(stats)
    ## Set the fitness function to run 50 generations
    ## Call the main function 50 times and pass all the genomes and the config file
    ## Generate a game based on all the genomes
    ## You can save this genome using pickle if needed
    winner = population.run(main, 50)

if __name__ == '__main__':
    filepath = os.path.dirname(__file__)
    config_file = os.path.join(filepath, 'config-feedforward.txt')
    run(config_file)
