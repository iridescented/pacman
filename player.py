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
    isCentered()
    __move()
    __canMove
    getGridInfo()
    setAnimationDetails ()
    isAtJunction
    queueMovement()
    reset()
    render()
    tick()
    """

    def __init__(self, name, app, home, sprite, ghostNo=0, ghostColor=None):
        self.name, self.app, self.home, self.ghostNo, self.ghostColor = name, app, home, ghostNo, ghostColor
        self.sprite = self.defaultSprite = self.__getSprite(pygame.image.load(sprite), 32, 32, 5, 2, ghostNo)
        self.reset()
        self.speed = SPEED
        self.setAnimDetails(20, (0.75, 0.15))
        self.ghost, self.ghostMode = False, "normal"
        if name != "Pacman":
            self.ghost = True
            self.frightenedSprite = self.__getSprite(pygame.image.load(sprite), 32, 32, 5, 2, 4)
            self.eatenSprite = self.__getSprite(pygame.image.load(sprite), 32, 32, 5, 2, 5)


############################ SETUP METHODS ###################################


    def includeAI(self, ai):
        self.ai = ai

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

    def isCentered(self):
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
            if gameboard(grid) == 3:
                currentGrid = [self.loc[0]//TILESIZE, self.loc[1]//TILESIZE]
                if gameboard(currentGrid) == 3 or self.ai.mode == "eaten":
                    return True
        else:
            return False

    def getGridInfo(self):
        """Returns info of the tiles surrounding the player"""
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
    def endCond(self):
        if self.pellets == 246:
            debug("END GAME YOU WIN")
            return True

    def __move(self, move=True):
        """Main logic for Movement, uses the value in queueMovement to move if the map permits it"""
        grid = self.getGridLoc()
        if self.ghost and self.ai.mode == "respawn":
            self.loc[1] = int(self.loc[1]+self.speed)
        if grid[0] == [28, 14] and self.isCentered():
            self.loc = [-16 + self.speed, 464]
            return False
        if grid[0] == [-1, 14] and self.isCentered():
            self.loc = [912 - self.speed, 464]
            return False
        if (not self.isCentered() and self.loc != self.homeLoc) or (not self.__canMove(grid[self.nextMovement]) and self.__canMove(grid[self.activeSprite])):
            self.loc = [int(self.loc[0]+self.velocity[0]), int(self.loc[1]+self.velocity[1])]
            return False
        elif not self.__canMove(grid[self.nextMovement]) and not self.__canMove(grid[self.activeSprite]):
            return False
        speed = (self.nextMovement > 2)*self.speed - (0 < self.nextMovement < 3)*self.speed
        self.velocity = [(self.nextMovement % 2 == 0)*speed, (self.nextMovement % 2 == 1)*speed]
        self.activeSprite = self.nextMovement
        if move:
            self.loc = [int(self.loc[0]+self.velocity[0]), int(self.loc[1]+self.velocity[1])]
        return True

    def queueMovement(self, direction, move=0):
        """Sets up next movement"""
        self.nextMovement = direction
        if move == 1:
            self.__move(False)
        elif move == 2:
            self.__move(True)

    def reset(self):
        """Resets the player to its initial state"""
        self.spriteAnim, self.activeSprite, self.nextMovement, self.pellets, self.velocity = 0, 0, 0, 0, [0, 0]
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
