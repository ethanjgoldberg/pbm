#!/usr/bin/python

import pygame, sys
import pygame.gfxdraw
from pygame.locals import *
import fileinput, math

COLOR = [(255,255,0),
         (0,255,0),
         (255,0,0)]

class PBM:
    def __init__(self):
        self.FPS = 40
        
        self.size = width, height = 1280, 760
        self.half = complex(width, height) / 2
        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.cam = 0j
        self.zoom = 1
        self.paused = False

        Z_BIG = 51.0 #change these
        Z_SMALL = 50.0

        self.Z_IN = Z_BIG / Z_SMALL #don't change these
        self.Z_OUT = Z_SMALL / Z_BIG

    def Draw(self, x, y, d, r, c):
        f = r == 1
        p = complex(x, y)
        c = COLOR[c]
        p *= self.zoom
        r *= self.zoom
        p -= self.cam - self.half
        if f:
            pygame.gfxdraw.filled_circle(self.screen, int(p.real), int(p.imag), max(int(r), 4), c)
        else:
            pygame.gfxdraw.circle(self.screen, int(p.real), int(p.imag), int(r), c)
            pygame.gfxdraw.pie(self.screen, int(p.real), int(p.imag), int(r), d - 10, d + 10, c)

    def DoStuff(self, forever=False):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    if event.key == K_SPACE:
                        self.paused = not self.paused
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.zoom *= self.Z_IN
                        self.cam *= self.Z_IN
                    if event.button == 5:
                        self.zoom *= self.Z_OUT
                        self.cam *= self.Z_OUT
            m = pygame.mouse.get_rel()
            self.cam += apply(complex, m)
            if not (self.paused or forever): break

    def Run(self):
        for line in fileinput.input():
            self.DoStuff()
            if line[0] == "\n":
                pygame.gfxdraw.circle(self.screen, self.half.real, self.half.imag, 4, (200,200,200,100))
                pygame.display.flip()
                self.screen.fill((0,0,0))
                self.clock.tick(self.FPS)
            elif line[0] == "#":
                pass
            elif line[0] == ">":
                print line
            else:
                apply(self.Draw, [eval(x) for x in line.split()])

        self.DoStuff(forever=True)

if __name__ == "__main__":
    P = PBM()
    P.Run()
