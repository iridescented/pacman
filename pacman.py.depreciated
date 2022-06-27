# IMPORTS
from threading import Thread
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

pacmanSpawn = (13.5, 23)
ghostSpawn = [(11, 13), (16, 13), (11, 15), (16, 15)]

# gameBoard size = 28*31
gameBoard = [
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
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 3, 3, 3, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 2, 2, 2, 2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
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
        self.app, self.home, self.sprite, self.name = app, coord, sprite, name
        self.reset()
        self.velocity = [0, 0]
        self.gridCoords = self.inCells(self.coord)
        self.nextMovement = "NONE"
        self.lastGrid = [[0, 0]]
        self.moveCooldown = 0
        if name == "Blinky":
            self.ghost = True
        else:
            self.ghost = False

    def render(self):
        self.app.screen.blit(self.activeSprite, (PADDING + self.coord[0]-TILESIZE//2,  PADDING + self.coord[1]-TILESIZE//2))
        # pygame.draw.circle(self.app.screen, RED, (PADDING + self.coord[0],  PADDING + self.coord[1]), 1)

    def reset(self):
        self.coord = [(self.home[0]+0.5) * TILESIZE, (self.home[1]+0.5)*TILESIZE]
        self.currentAnim = 0
        self.activeSpriteState = 0
        self.activeSprite = self.sprite[self.currentAnim][self.activeSpriteState]
        self.justSpawned = True
        self.velocity = [0, 0]

    def queueMovement(self, direction):
        self.nextMovement = direction
        if self.justSpawned:
            if self.nextMovement == "LEFT ":
                self.velocity = [-SPEED, 0]
                self.activeSpriteState = 2
            elif self.nextMovement == "RIGHT":
                self.velocity = [SPEED, 0]
                self.activeSpriteState = 4
            self.justSpawned = False

    def move(self, gridCoords):
        self.gridCoords[0] = []
        self.gridCoords[0] = gridCoords
        match self.nextMovement:
            case "UP   ":
                if gameBoard[gridCoords[1]-1][gridCoords[0]] == 1:
                    self.velocity = [0, -SPEED]
                    self.coord[0] = int(self.coord[0]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 1
            case "DOWN ":
                if gameBoard[gridCoords[1]+1][gridCoords[0]] == 1:
                    self.velocity = [0, SPEED]
                    self.coord[0] = int(self.coord[0]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 3
            case "LEFT ":
                if gameBoard[gridCoords[1]][gridCoords[0]-1] == 1:
                    self.velocity = [-SPEED, 0]
                    self.coord[1] = int(self.coord[1]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 2
            case "RIGHT":
                if gameBoard[gridCoords[1]][gridCoords[0]+1] == 1:
                    self.velocity = [SPEED, 0]
                    self.coord[1] = int(self.coord[1]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 4

    def ghostMove(self, Ai):
        if not self.ghost:
            return False
        if self.moveCooldown == 0:
            oldMovement = self.nextMovement
            self.queueMovement(Ai.chase())
            if self.nextMovement != oldMovement:
                self.moveCooldown = 2
        else:
            self.moveCooldown -= 1

    def animate(self):
        self.currentAnim += 1
        self.currentAnim %= 20
        self.activeSprite = self.sprite[self.currentAnim//15][self.activeSpriteState]
        pass

    def inCells(self, coords):
        cells = []
        posChecks = [[coords[0], coords[1]-TILESIZE//2+1], [coords[0]-TILESIZE//2+1, coords[1]], [coords[0], coords[1]+TILESIZE//2-1], [coords[0]+TILESIZE//2-1, coords[1]]]
        for i in posChecks:
            if not [int(i[0]//TILESIZE), int(i[1]//TILESIZE)] in cells:
                cells.append([int(i[0]//TILESIZE), int(i[1]//TILESIZE)])
        return cells

    def tick(self, Ai=None):
        tempGridCells = self.inCells(self.coord)
        self.ghostMove(Ai)
        if len(tempGridCells) == 1:
            self.move(tempGridCells[0])
        tempCoord = [int(self.coord[0]+self.velocity[0]), int(self.coord[1]+self.velocity[1])]
        tempGridCells = self.inCells(tempCoord)
        for locations in tempGridCells:
            if gameBoard[locations[1]][locations[0]] == 0:
                return False
        self.coord = tempCoord
        self.animate()

##########################################################################
############################ AI ENGINE ###################################
##########################################################################


class AI_Engine:
    """AI Engine"""

    def __init__(self, ghost, pacman, targetMode):
        self.pac = pacman
        self.ghost = ghost
        self.targetMode = 1

    # Check all sides
    # Remove backside
    # Check which is closer
    #
    def chase(self):

        def distToPacman(location):
            if self.targetMode == 1:
                target = self.pac.coord
            return math.sqrt(((target[0]-location[0])**2) + ((target[1]-location[1])**2))
        gridDistance = [distToPacman((self.ghost.coord[0], self.ghost.coord[1]-TILESIZE)), distToPacman((self.ghost.coord[0]-TILESIZE, self.ghost.coord[1])),
                        distToPacman((self.ghost.coord[0], self.ghost.coord[1]+TILESIZE)), distToPacman((self.ghost.coord[0]+TILESIZE, self.ghost.coord[1]))]
        gC = [self.ghost.gridCoords[0][1], self.ghost.gridCoords[0][0]]
        grid = [gameBoard[gC[0]-1][gC[1]], gameBoard[gC[0]][gC[1]-1], gameBoard[gC[0]+1][gC[1]], gameBoard[gC[0]][gC[1]+1]]
        grid[(self.ghost.activeSpriteState - 3) % 4] = 0
        bestDirection = None
        bestDistance = 1000
        for i in range(0, 4):
            if grid[i] == 1 and gridDistance[i] < bestDistance:
                bestDistance = gridDistance[i]
                bestDirection = i

        if bestDirection == 0:
            go = "UP   "
        elif bestDirection == 1:
            go = "LEFT "
        elif bestDirection == 2:
            go = "DOWN "
        elif bestDirection == 3:
            go = "RIGHT"
        return go

    def scatter(self):
        pass

    def frightened(self):
        pass

    def eaten(self):
        pass

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
        self.pacman = Entity(self, pacmanSpawn, self.get_sprite(pygame.image.load(PACMAN), 32, 32, 5, 2), "Pacman")
        self.blinky = Entity(self, ghostSpawn[0], self.get_sprite(pygame.image.load(BLINKY), 32, 32, 5, 2), "Blinky")
        self.blinkyAI = AI_Engine(self.blinky, self.pacman, 1)

############################ HELPER METHODS ##################################

    def updateState(self, nextState):
        self.state = nextState
        debug("*State Updated to: " + nextState)

    def renderGrid(self):
        if not OVERLAY_ENABLED:
            return
        for x in range(0, MAZE_WIDTH, TILESIZE):
            for y in range(0, MAZE_HEIGHT, TILESIZE):
                match gameBoard[y//TILESIZE][x//TILESIZE]:
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
        stringSize = string.get_size()
        if pos[0] < 0:
            pos[0] = WINDOW_WIDTH+pos[0]-stringSize[0]
        if pos[1] < 0:
            pos[1] = WINDOW_HEIGHT+pos[1]-stringSize[1]
        if center:
            pos = [pos[0]-stringSize[0]//2, pos[1]-stringSize[1]//2]
        screen.blit(string, pos)

########################### INIT METHODS ####################################

    def get_sprite(self, sheet, w, h, frames, animationFrames):
        allframes = []
        for anim in range(0, animationFrames, 1):
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
                        self.pacman.queueMovement("RIGHT")
                    case pygame.K_a:
                        self.pacman.queueMovement("LEFT ")
                    case pygame.K_s:
                        self.pacman.queueMovement("DOWN ")
                    case pygame.K_w:
                        self.pacman.queueMovement("UP   ")
                    case pygame.K_RIGHT:
                        self.blinky.queueMovement("RIGHT")
                    case pygame.K_LEFT:
                        self.blinky.queueMovement("LEFT ")
                    case pygame.K_DOWN:
                        self.blinky.queueMovement("DOWN ")
                    case pygame.K_UP:
                        self.blinky.queueMovement("UP   ")
                    case pygame.K_q:
                        self.running = False
                    case pygame.K_e:
                        self.blinkyAI.chase()
                    case pygame.K_r:
                        self.pacman.reset()
                        self.blinky.reset()

    def renderGame(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (PADDING, PADDING))
        self.renderGrid()
        self.pacman.render()
        self.blinky.render()
        self.renderText("NEXT MOVEMENT: "+self.pacman.nextMovement, self.screen, [-PADDING, -PADDING//4], RED)
        pygame.display.update()

    def tick(self):
        self.pacman.tick()
        self.blinky.tick(self.blinkyAI)
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
