from settings import debug, TILESIZE, SPEED
from player import gameboard
from math import sqrt
from random import randint
import pygame

##########################################################################
############################ AI ENGINE ###################################
##########################################################################


class AiEngine:
    """Redesign of AI Engine"""

    def __init__(self, ghost, pac, ghost2=None):
        self.pac, self.ghost, self.ghost2 = pac, ghost, ghost2
        self.mode, self.time = "leavespawn", pygame.time.get_ticks()
        self.scatterTime, self.chaseTime, self.frightenedTime = 7, 20, 8
        self.enabled = False
        self.target = [0, 0]
############################ SETUP METHODS ###################################

    def enableGhost(self):
        self.enabled = True

############################ HELPER METHODS ##################################

    def __distance(self, target, player):
        return sqrt(((target[0]-player[0])**2) + ((target[1]-player[1])**2))

    def __shift(self, grid, direction, dist):
        return [grid[0] + (direction == 1)*dist - (direction == 3)*dist, grid[1] + (direction == 4)*dist - (direction == 2)*dist]


########################### UPDATE METHODS ####################################

    def __move(self, targetGrid):
        bestDirection = 0
        bestDistance = 1000
        ghostGrid = self.ghost.getGridLoc()
        gridData = self.ghost.getGridInfo()
        for i in range(1, len(gridData)):
            if gridData[i] == True and self.__distance(targetGrid, ghostGrid[i]) < bestDistance and i != (self.ghost.activeSprite + 1) % 4+1:
                bestDirection = i
                bestDistance = self.__distance(targetGrid, ghostGrid[i])
        return bestDirection

    def __leaveSpawn(self):
        self.target = [14, 12]
        return self.__move(self.target)

    def __chase(self):
        pacGrid = [self.pac.loc[0]//TILESIZE + 0.5, self.pac.loc[1]//TILESIZE + 0.5]
        self.target = pacGrid
        if self.ghost.ghostNo == 1:
            tempLoc = self.__shift(pacGrid, self.pac.activeSprite, 2)
            distance = [self.ghost2.loc[0]//TILESIZE - tempLoc[0], self.ghost2.loc[1]//TILESIZE - tempLoc[1]]
            self.target = [self.ghost2.loc[0] + 2 * distance[0], self.ghost2.loc[1] + 2 * distance[1]]
        elif self.ghost.ghostNo == 2:
            self.target = self.__shift(pacGrid, self.pac.activeSprite, 4)
        elif self.ghost.ghostNo == 3:
            if self.__distance(self.ghost.loc, self.pac.loc) <= 8*TILESIZE:
                self.target = (0, 32)
        return self.__move(self.target)

    def __scatter(self, corner):
        if corner == 0:
            self.target = (25, -4)
        elif corner == 2:
            self.target = (2, -4)
        elif corner == 1:
            self.target = (27, 32)
        elif corner == 3:
            self.target = (0, 32)
        return self.__move(self.target)

    def __frightened(self):
        direction = (self.ghost.activeSprite + 1) % 4+1
        while direction == (self.ghost.activeSprite + 1) % 4+1:
            direction = randint(1, 4)
        return direction

    def __eaten(self):
        self.target = [13, 11]
        return self.__move(self.target)

    def enableFrightened(self):
        self.mode = "frightened"
        self.time = pygame.time.get_ticks()
        self.ghost.sprite = self.ghost.frightenedSprite
        self.ghost.speed = 0.5*SPEED
        self.ghost.queueMovement((self.ghost.activeSprite + 1) % 4+1, True)

    def renderTarget(self, font, screen):
        string = font.render("X", False, self.ghost.ghostColor)
        screen.blit(string, (self.target[0]*TILESIZE + TILESIZE//2, self.target[1]*TILESIZE + TILESIZE//2))

    def reset(self):
        self.ghost.reset()
        self.mode, self.time = "leavespawn", pygame.time.get_ticks()

    def endCond(self):
        pacGrid = [self.pac.loc[0]//TILESIZE, self.pac.loc[1]//TILESIZE]
        ghostGrid = [self.ghost.loc[0]//TILESIZE, self.ghost.loc[1]//TILESIZE]
        if pacGrid == ghostGrid:
            if self.mode == "frightened":
                self.mode = "eaten"
                self.time = pygame.time.get_ticks()
                self.ghost.sprite = self.ghost.eatenSprite
                self.ghost.speed = SPEED
            elif self.mode != "eaten":
                return True
        return False

    def tick(self):
        if not self.enabled:
            self.ghost.tick()
            return
        if self.mode == "eaten" and self.ghost.isCentered():
            ghostGrid = self.ghost.getGridLoc()
            if ghostGrid[0] == self.target:
                self.ghost.queueMovement(3, True)
                self.mode = "respawn"
            else:
                self.ghost.queueMovement(self.__eaten())
        elif self.mode == "respawn":
            if self.ghost.getGridLoc()[0] != self.target:
                self.ghost.sprite = self.ghost.defaultSprite
                self.mode = "leavespawn"
        elif self.mode == "frightened":
            if pygame.time.get_ticks() - self.time >= self.frightenedTime*1000:
                self.ghost.speed = SPEED
                self.ghost.sprite = self.ghost.defaultSprite
                self.time = pygame.time.get_ticks()
                self.mode = "chase"
                self.ghost.queueMovement((self.ghost.activeSprite + 1) % 4+1, False)
            elif self.ghost.isAtJunction():
                self.ghost.queueMovement(self.__frightened())
        elif self.ghost.isAtJunction():
            if self.mode == "leavespawn":
                ghostGrid = self.ghost.getGridLoc()
                if ghostGrid[0][1] == 11:
                    self.mode = "scatter"
                    self.__scatter(self.ghost.ghostNo)
                else:
                    self.ghost.queueMovement(self.__leaveSpawn())
            elif self.mode == "scatter":
                if pygame.time.get_ticks() - self.time >= self.scatterTime*1000:
                    self.time = pygame.time.get_ticks()
                    self.mode = "chase"
                    self.ghost.queueMovement((self.ghost.activeSprite + 1) % 4+1, False)
                else:
                    self.ghost.queueMovement(self.__scatter(self.ghost.ghostNo))
            elif self.mode == "chase":
                if pygame.time.get_ticks() - self.time >= self.chaseTime*1000:
                    self.time = pygame.time.get_ticks()
                    self.mode = "scatter"
                    self.ghost.queueMovement((self.ghost.activeSprite + 1) % 4+1, False)
                else:
                    self.ghost.queueMovement(self.__chase())
        self.ghost.tick()
