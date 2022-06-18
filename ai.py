from settings import debug, TILESIZE
from player import gameboard
from math import sqrt
import pygame

##########################################################################
############################ AI ENGINE ###################################
##########################################################################


class AiEngine:
    """Redesign of AI Engine"""

    def __init__(self, ghost, pac, ghost2=None):
        self.pac, self.ghost, self.ghost2 = pac, ghost, ghost2
        self.mode, self.time = "leavespawn", pygame.time.get_ticks()
        self.scatterTime, self.chaseTime = 7, 20
        self.enabled = False
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
        self.target = (14, 0)
        return self.__move(self.target)

    def __chase(self):
        pacGrid = [self.pac.loc[0]//TILESIZE, self.pac.loc[1]//TILESIZE]
        self.target = pacGrid
        if self.ghost.ghostNo == 1:
            tempLoc = self.__shift(pacGrid, self.pac.activeSprite, 2)
            distance = [self.ghost2.loc[0] - tempLoc[0], self.ghost2.loc[1] - tempLoc[1]]
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
        pass

    def __eaten(self):
        pass

    def renderTarget(self):
        string = self.font.render("X", False, self.ghost.ghostColor)

    def reset(self):
        self.ghost.reset()
        self.mode, self.time = "leavespawn", pygame.time.get_ticks()

    def endCond(self):
        pacGrid = [self.pac.loc[0]//TILESIZE, self.pac.loc[1]//TILESIZE]
        ghostGrid = [self.ghost.loc[0]//TILESIZE, self.ghost.loc[1]//TILESIZE]
        if pacGrid == ghostGrid:
            return True
        return False

    def tick(self):
        if self.ghost.isAtJunction() and self.enabled:
            if self.mode == "leavespawn":
                gridLoc = self.ghost.getGridLoc()
                gridLoc = gameboard(gridLoc[0])
                if gridLoc != 3:
                    self.mode = "scatter"
                else:
                    self.ghost.queueMovement(self.__leaveSpawn())
            elif self.mode == "scatter":
                if pygame.time.get_ticks() - self.time >= self.scatterTime*1000:
                    self.time = pygame.time.get_ticks()
                    self.mode = "chase"
                    self.ghost.queueMovement((self.ghost.activeSprite + 1) % 4+1, True)
                else:
                    self.ghost.queueMovement(self.__scatter(self.ghost.ghostNo))
            elif self.mode == "chase":
                if pygame.time.get_ticks() - self.time >= self.chaseTime*1000:
                    self.time = pygame.time.get_ticks()
                    self.mode = "scatter"
                    self.ghost.queueMovement((self.ghost.activeSprite + 1) % 4+1, True)
                else:
                    self.ghost.queueMovement(self.__chase())
        self.ghost.tick()


'''
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
            return sqrt(((target[0]-location[0])**2) + ((target[1]-location[1])**2))
        gridDistance = [distToPacman((self.ghost.coord[0], self.ghost.coord[1]-TILESIZE)), distToPacman((self.ghost.coord[0]-TILESIZE, self.ghost.coord[1])),
                        distToPacman((self.ghost.coord[0], self.ghost.coord[1]+TILESIZE)), distToPacman((self.ghost.coord[0]+TILESIZE, self.ghost.coord[1]))]
        gC = [self.ghost.gridCoords[0][1], self.ghost.gridCoords[0][0]]
        grid = [GAMEBOARD[gC[0]-1][gC[1]], GAMEBOARD[gC[0]][gC[1]-1], GAMEBOARD[gC[0]+1][gC[1]], GAMEBOARD[gC[0]][gC[1]+1]]
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
'''
