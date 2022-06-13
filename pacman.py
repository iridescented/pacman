# GOAL FOR TODAY
# -Working UI


# IMPORTS
from doctest import FAIL_FAST
from queue import Empty
from turtle import screensize
from unicodedata import name
import pygame
import sys
import math
import random
from settings import *

# DEFINITIONS
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
LGRAY = (211, 211, 211)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TILESIZE = SCALE
PADDING = FONTSIZE * 2
MAZE_WIDTH = 28*TILESIZE
MAZE_HEIGHT = 31*TILESIZE
WINDOW_WIDTH = MAZE_WIDTH + 2*PADDING
WINDOW_HEIGHT = MAZE_HEIGHT + 2*PADDING

pacmanspawn = (13.5, 23)
ghostspawn = [(11, 13), (16, 13), (11, 15), (16, 15)]

# gameboard size = 28*31
gameboard = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def debug(string):
    if DEBUG_ENABLED == True:
        print(string)

##########################################################################
############################ ENTITY CLASS ################################
##########################################################################


class Entity:
    """Entities class is used as a base class for all entities, including their coordinates, """

    def __init__(self, app, coord, sprite, name):
        self.app = app
        self.home = coord
        self.sprite = sprite
        self.name = name
        self.reset()
        self.velocity = [0, 0]
        self.gridcoords = None
        self.nextmovement = "NONE"

    def render(self):
        self.app.screen.blit(self.activeSprite, (PADDING + self.coord[0]-TILESIZE//2,  PADDING + self.coord[1]-TILESIZE//2))
        # pygame.draw.circle(self.app.screen, RED, (PADDING + self.coord[0],  PADDING + self.coord[1]), 1)

    def reset(self):
        self.coord = [(self.home[0]+0.5) * TILESIZE, (self.home[1]+0.5)*TILESIZE]
        self.currentAnim = 0
        self.activeSpriteState = 0
        self.activeSprite = self.sprite[self.currentAnim][self.activeSpriteState]
        self.justspawned = True
        self.velocity = [0, 0]

    def queuemovement(self, direction):
        self.nextmovement = direction
        if self.justspawned:
            if self.nextmovement == "LEFT ":
                self.velocity = [-SPEED, 0]
                self.activeSpriteState = 3
            elif self.nextmovement == "RIGHT":
                self.velocity = [SPEED, 0]
                self.activeSpriteState = 1
            self.justspawned = False

    def move(self, gridcoords):
        self.gridcoords = gridcoords
        match self.nextmovement:
            case "UP   ":
                if gameboard[gridcoords[1]-1][gridcoords[0]] == 1:
                    self.velocity = [0, -SPEED]
                    self.coord[0] = int(self.coord[0]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 4
            case "DOWN ":
                if gameboard[gridcoords[1]+1][gridcoords[0]] == 1:
                    self.velocity = [0, SPEED]
                    self.coord[0] = int(self.coord[0]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 2
            case "LEFT ":
                if gameboard[gridcoords[1]][gridcoords[0]-1] == 1:
                    self.velocity = [-SPEED, 0]
                    self.coord[1] = int(self.coord[1]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 3
            case "RIGHT":
                if gameboard[gridcoords[1]][gridcoords[0]+1] == 1:
                    self.velocity = [SPEED, 0]
                    self.coord[1] = int(self.coord[1]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 1

    def animate(self):
        self.currentAnim += 1
        self.currentAnim %= 20
        self.activeSprite = self.sprite[self.currentAnim//15][self.activeSpriteState]
        pass

    def incells(self, coords):
        cells = []
        poschecks = [[coords[0], coords[1]-TILESIZE//2+1], [coords[0]-TILESIZE//2+1, coords[1]], [coords[0], coords[1]+TILESIZE//2-1], [coords[0]+TILESIZE//2-1, coords[1]]]
        for i in poschecks:
            if not [int(i[0]//TILESIZE), int(i[1]//TILESIZE)] in cells:
                cells.append([int(i[0]//TILESIZE), int(i[1]//TILESIZE)])
        return cells

    def tick(self):
        tempgridcells = self.incells(self.coord)
        if len(tempgridcells) == 1:
            self.move(tempgridcells[0])
        tempcoord = [int(self.coord[0]+self.velocity[0]), int(self.coord[1]+self.velocity[1])]
        tempgridcells = self.incells(tempcoord)
        for locations in tempgridcells:
            if gameboard[locations[1]][locations[0]] == 0:
                return False
        self.coord = tempcoord
        self.animate()

##########################################################################
############################ GAME CLASS ##################################
##########################################################################


class Game:
    """Main Game Engine """

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('PACMAN')

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.overlay = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.background = pygame.transform.scale(pygame.image.load('Assets/maze.png'), (MAZE_WIDTH, MAZE_HEIGHT))
        self.font = pygame.font.SysFont(FONTNAME, FONTSIZE)
        ###Switches###
        self.running = True
        self.updateState("startup")

        ###Entities###
        self.pacman = Entity(self, pacmanspawn, self.get_sprite(pygame.image.load(PACMAN), 32, 32, 5, 2), "Pacman")
        self.blinky = Entity(self, ghostspawn[0], self.get_sprite(pygame.image.load(PACMAN), 32, 32, 5, 2), "Blinky")

############################ HELPER METHODS ##################################

    def updateState(self, nextState):
        self.state = nextState
        debug("*State Updated to: " + nextState)

    def renderGrid(self):
        if not OVERLAY_ENABLED:
            return
        for x in range(0, MAZE_WIDTH, TILESIZE):
            for y in range(0, MAZE_HEIGHT, TILESIZE):
                match gameboard[y//TILESIZE][x//TILESIZE]:
                    case 1:
                        self.overlay.set_alpha(50)
                        self.overlay.fill(GREEN)
                    case default:
                        self.overlay.set_alpha(0)
                        self.overlay.fill(RED)
                self.screen.blit(self.overlay, (PADDING+x, PADDING+y))
        for i in range(0, MAZE_HEIGHT + TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LGRAY, (PADDING, PADDING+i), (PADDING+MAZE_WIDTH, PADDING+i))
        for i in range(0, MAZE_WIDTH + TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LGRAY, (PADDING+i, PADDING), (PADDING+i, PADDING+MAZE_HEIGHT))

    def renderText(self, text, screen, pos, colour, center=False):
        string = self.font.render(text, False, colour)
        string_size = string.get_size()
        if pos[0] < 0:
            pos[0] = WINDOW_WIDTH+pos[0]-string_size[0]
        if pos[1] < 0:
            pos[1] = WINDOW_HEIGHT+pos[1]-string_size[1]
        if center:
            pos = [pos[0]-string_size[0]//2, pos[1]-string_size[1]//2]
        screen.blit(string, pos)

########################### INIT METHODS ####################################

    def get_sprite(self, sheet, w, h, frames, animationframes):
        allframes = []
        for anim in range(0, animationframes, 1):
            images = []
            for frame in range(0, frames, 1):
                image = pygame.Surface((w, h)).convert_alpha()
                image.blit(sheet, (0, 0), (frame*w, anim*h, w, h))
                image = pygame.transform.scale(image, (SCALE, SCALE))
                image.set_colorkey(BLACK)
                images.append(image)
            allframes.append(images)
        return allframes

########################### UPDATE METHODS ####################################

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_d:
                        self.pacman.queuemovement("RIGHT")
                    case pygame.K_a:
                        self.pacman.queuemovement("LEFT ")
                    case pygame.K_s:
                        self.pacman.queuemovement("DOWN ")
                    case pygame.K_w:
                        self.pacman.queuemovement("UP   ")
                    case pygame.K_q:
                        self.running = False
                    case pygame.K_e:
                        gridcells = self.pacman.incells(self.pacman.coord)
                        for value in gridcells:
                            debug(str(value)+": "+str(gameboard[value[1]][value[0]]))
                    case pygame.K_r:
                        self.pacman.reset()
                    case pygame.K_v:
                        debug(self.pacman.velocity)

    def renderGame(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (PADDING, PADDING))
        self.renderGrid()
        self.pacman.render()
        self.blinky.render()
        self.renderText("NEXT MOVEMENT: "+self.pacman.nextmovement, self.screen, [-PADDING, -PADDING//4], RED)
        pygame.display.update()
        pass

    def tick(self):
        self.pacman.tick()
        self.renderGame()

    def run(self):
        debug("--Main Sequence Initialized--")
        while self.running:
            if self.state == "startup":
                self.renderGame()
                self.updateState("play")
                debug("--Start Sequence Initialized--")
            elif self.state == "play":
                self.tick()
            self.clock.tick(FPS)
            self.checkEvents()
            pygame.display.update()
        pygame.quit()
        sys.exit()

########################### MAIN SEQUENCE ####################################


Pac = Game()
Pac.run()
