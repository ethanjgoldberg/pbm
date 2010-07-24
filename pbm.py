#!/usr/bin/python

import pygame, sys
import pygame.gfxdraw
from pygame.locals import *
import fileinput, math


FPS = 20
COLOR = [(0,0,255),
         (0,255,0),
         (255,0,0)]


size = width, height = 1280, 760
half = complex(width, height) / 2

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

cam = 0j
zoom = 1

Z_BIG = 51.0 #change these
Z_SMALL = 50.0

Z_IN = Z_BIG / Z_SMALL #don't change these
Z_OUT = Z_SMALL / Z_BIG

def Draw(x, y, d, r, c):
    f = r == 1
    p = complex(x, y)
    c = COLOR[c]
    p *= zoom
    r *= zoom
    p -= cam - half
    if f:
        pygame.gfxdraw.filled_circle(screen, int(p.real), int(p.imag), int(r), c)
    else:
        pygame.gfxdraw.circle(screen, int(p.real), int(p.imag), int(r), c)
        pygame.gfxdraw.pie(screen, int(p.real), int(p.imag), int(r), d - 10, d + 10, c)
        
for line in fileinput.input():
    first = True
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                zoom *= Z_IN
                cam *= Z_IN
            if event.button == 5:
                zoom *= Z_OUT
                cam *= Z_OUT
    m = pygame.mouse.get_rel()
    cam += apply(complex, m)
    if line[0] == "\n":
        pygame.gfxdraw.circle(screen, half.real, half.imag, 4, (200,200,200,100))
        pygame.display.flip()
        screen.fill((0,0,0))
        clock.tick(FPS)
    elif line[0] == "#":
        pass
    elif line[0] == ">":
        print line
    else:
        apply(Draw, [eval(x) for x in line.split()])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()    
