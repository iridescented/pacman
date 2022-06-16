from settings import *
from math import sqrt

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
