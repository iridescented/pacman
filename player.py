from settings import debug, PADDING, GAMEBOARD, SCALE, BLACK, TILESIZE, SPEED
import pygame


def STS(x, y):
    """Shifts coordinates by padding to align to screen coordinates"""
    return (PADDING + x, PADDING + y)


def gameboard(grid):
    return GAMEBOARD[int(grid[1])][int(grid[0])]
##########################################################################
############################ Player CLASS ################################
##########################################################################


class Player:
    """Player Class for all entities
    __init__()
    __getSprite()
    getGridLoc()
    __animate()
    __isCentered()
    __move()
    __canMove
    getGridInfo()
    setAnimationDetails()
    isAtJunction
    queueMovement()
    reset()
    render()
    tick()
    """

    def __init__(self, name, app, home, sprite, ghostNo=0, ghostColor=None):
        self.name, self.app, self.home, self.ghostNo, self.ghostColor = name, app, home, ghostNo, ghostColor
        self.sprite = self.__getSprite(pygame.image.load(sprite), 32, 32, 5, 2, ghostNo)
        self.reset()
        self.setAnimDetails(20, (0.75, 0.15))
        self.ghost = False
        if name != "Pacman":
            self.ghost = True

############################ SETUP METHODS ###################################

    def setAnimDetails(self, totalFrames, framePercent):
        """Setup for Animation Values"""
        self.animTotalFrames, self.animFramePercent = totalFrames, framePercent

############################ HELPER METHODS ##################################

    def __getSprite(self, sheet, w, h, frames, animationFrames, startPos):
        """Generates Sprite array from a Sprite Sheet"""
        allframes = []
        for anim in range(0, animationFrames, 1):
            images = []
            for frame in range(0, frames, 1):
                image = pygame.Surface((w, h)).convert_alpha()
                image.blit(sheet, (0, 0), (frame*w, ((startPos * 2 + anim) * h), w, h))
                image = pygame.transform.scale(image, (SCALE, SCALE))
                image.set_colorkey(BLACK)
                images.append(image)
            allframes.append(images)
        return allframes

    def getGridLoc(self):
        """Returns all 5 grid locations centered around player position"""
        currentGrid = [self.loc[0]//TILESIZE, self.loc[1]//TILESIZE]
        leftGrid = [(self.loc[0]-TILESIZE)//TILESIZE, self.loc[1]//TILESIZE]
        rightGrid = [(self.loc[0]+TILESIZE)//TILESIZE, self.loc[1]//TILESIZE]
        upGrid = [self.loc[0]//TILESIZE, (self.loc[1]-TILESIZE)//TILESIZE]
        downGrid = [self.loc[0]//TILESIZE, (self.loc[1]+TILESIZE)//TILESIZE]
        return [currentGrid, upGrid, leftGrid, downGrid, rightGrid]

    def __animate(self):
        """Animates the player using the sprite"""
        self.spriteAnim += 1
        self.spriteAnim %= self.animTotalFrames
        self.drawnSprite = self.sprite[int(self.spriteAnim//(self.animFramePercent[0]*self.animTotalFrames))][self.activeSprite]

    def __isCentered(self):
        """Returns True if player is at center of Tile"""
        if (self.loc[0] % TILESIZE == TILESIZE//2 and self.loc[1] % TILESIZE == TILESIZE//2):
            return True
        return False

    def __canMove(self, grid):
        """Returns whether the player can move or not to that tile"""
        if grid == [28, 14] or grid == [-1, 14]:
            return True
        elif grid == [28, 13] or grid == [-1, 13] or grid == [28, 15] or grid == [-1, 15]:
            return False
        elif 2 >= gameboard(grid) > 0:
            return True
        elif self.ghost:
            currentGrid = [self.loc[0]//TILESIZE, self.loc[1]//TILESIZE]
            if gameboard(currentGrid) == gameboard(grid) == 3:
                return True
        else:
            return False

    def getGridInfo(self):
        grid = self.getGridLoc()
        gridInfo = []
        for i in grid:
            gridInfo.append(self.__canMove(i))
        return gridInfo

    def isAtJunction(self):
        """Returns true if player is at a junction"""
        currentGrid = [self.loc[0]//TILESIZE, self.loc[1]//TILESIZE]
        if currentGrid == [28, 14] or currentGrid == [-1, 14]:
            return False
        if gameboard(currentGrid) == 2 or gameboard(currentGrid) == 3:
            return True
        return False

########################### UPDATE METHODS ####################################

    def __move(self, forced=False):
        """Main logic for Movement, uses the value in queueMovement to move if the map permits it"""
        grid = self.getGridLoc()

        if grid[0] == [28, 14] and self.__isCentered():
            self.loc = [-16 + SPEED, 464]
            return False
        if grid[0] == [-1, 14] and self.__isCentered():
            self.loc = [912 - SPEED, 464]
            return False
        if (not self.__isCentered() and self.loc != self.homeLoc) or (not self.__canMove(grid[self.nextMovement]) and self.__canMove(grid[self.activeSprite])):
            self.loc = [int(self.loc[0]+self.velocity[0]), int(self.loc[1]+self.velocity[1])]
            return False
        elif not self.__canMove(grid[self.nextMovement]) and not self.__canMove(grid[self.activeSprite]):
            return False
        speed = (self.nextMovement > 2)*SPEED - (0 < self.nextMovement < 3)*SPEED
        self.velocity = [(self.nextMovement % 2 == 0)*speed, (self.nextMovement % 2 == 1)*speed]
        self.activeSprite = self.nextMovement
        if not forced:
            self.loc = [int(self.loc[0]+self.velocity[0]), int(self.loc[1]+self.velocity[1])]
        return True

    def queueMovement(self, direction, forced=False):
        """Sets up next movement"""
        self.nextMovement = direction
        if forced:
            self.__move(True)

    def reset(self):
        """Resets the player to its initial state"""
        self.spriteAnim, self.activeSprite, self.nextMovement, self.velocity = 0, 0, 0, [0, 0]
        self.drawnSprite = self.sprite[self.spriteAnim][self.activeSprite]
        self.homeLoc = self.loc = [(self.home[0]+0.5) * TILESIZE, (self.home[1]+0.5)*TILESIZE]

    def render(self):
        """Renders the player to the screen"""
        self.app.screen.blit(self.drawnSprite, STS(self.loc[0]-TILESIZE//2, self.loc[1]-TILESIZE//2))
        # pygame.draw.circle(self.app.screen, RED, (PADDING + self.loc[0],  PADDING + self.coord[1]), 1)

    def tick(self):
        """Called every tick while game is active"""
        self.__move()
        self.__animate()


'''
class Entity:
    """Entities class is used as a base class for all entities"""

    def __init__(self, app, coord, sprite, name):
        self.app, self.home, self.sprite, self.name = app, coord, sprite, name
        self.reset()
        self.gridCoords = self.inCells(self.coord)
        self.nextMovement = "NONE"
        self.lastGrid = [[0, 0]]
        self.moveCooldown = 0

    def render(self):
        self.app.screen.blit(self.activeSprite, (PADDING + self.coord[0]-TILESIZE//2,  PADDING + self.coord[1]-TILESIZE//2))
        # pygame.draw.circle(self.app.screen, RED, (PADDING + self.coord[0],  PADDING + self.coord[1]), 1)

    def reset(self):
        self.coord = [(self.home[0]+0.5) * TILESIZE, (self.home[1]+0.5)*TILESIZE]
        self.currentAnim = self.activeSpriteState = 0
        self.activeSprite = self.sprite[self.currentAnim][self.activeSpriteState]
        self.justSpawned = True
        self.velocity = [0, 0]

    def queueMovement(self, direction):
        self.nextMovement = direction
        if self.justSpawned:
            if self.nextMovement == 2:
                self.velocity = [-SPEED, 0]
                self.activeSpriteState = 2
            elif self.nextMovement == 4:
                self.velocity = [SPEED, 0]
                self.activeSpriteState = 4
            self.justSpawned = False

    def move(self, gridCoords):
        self.gridCoords[0] = []
        self.gridCoords[0] = gridCoords
        match self.nextMovement:
            case 1:
                if GAMEBOARD[gridCoords[1]-1][gridCoords[0]] == 1:
                    self.velocity = [0, -SPEED]
                    self.coord[0] = int(self.coord[0]//TILESIZE*TILESIZE+TILESIZE//2)
            case 2:
                if GAMEBOARD[gridCoords[1]][gridCoords[0]-1] == 1:
                    self.velocity = [-SPEED, 0]
                    self.coord[1] = int(self.coord[1]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 2
            case 3:
                if GAMEBOARD[gridCoords[1]+1][gridCoords[0]] == 1:
                    self.velocity = [0, SPEED]
                    self.coord[0] = int(self.coord[0]//TILESIZE*TILESIZE+TILESIZE//2)
                    self.activeSpriteState = 3
            case 4:
                if GAMEBOARD[gridCoords[1]][gridCoords[0]+1] == 1:
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
            if GAMEBOARD[locations[1]][locations[0]] == 0:
                return False
        self.coord = tempCoord
        self.animate()
'''
