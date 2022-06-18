# IMPORTS
from threading import Thread
import pygame
import sys
from ai import AiEngine
from player import Player
from settings import debug, PADDING, GAMEBOARD, BLACK, TILESIZE, FONTNAME, FONTSIZE, WINDOW_HEIGHT, WINDOW_WIDTH, MAZE_HEIGHT, MAZE_WIDTH, PACMAN, GHOST, OVERLAY_ENABLED, FPS, GREEN, RED, LGRAY, PINK, YELLOW, GHOSTCOLOR


# DEFINITIONS


PACMAN_SPAWN = (13.5, 23)
GHOST_SPAWN = [(11, 13), (16, 13), (11, 15), (16, 15)]

##########################################################################
############################ GAME CLASS ##################################
##########################################################################


class Game:
    """Main Game Engine
    __init__()
    __updateState()
    __renderGrid()
    __renderText()
    __checkEvents()
    __renderGame()
    __tick()
    run()
    """

    def __init__(self):
        ###Basic Initialization###
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('PACMAN')
        self.font = pygame.font.SysFont(FONTNAME, FONTSIZE)
        ###Setup Variables###
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.overlay = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.background = pygame.transform.scale(pygame.image.load('Assets/maze.png'), (MAZE_WIDTH, MAZE_HEIGHT))
        ###Switches###
        self.running = True
        self.__updateState("startup")
        ###Entities###
        self.pacman = Player("Pacman", self, PACMAN_SPAWN, PACMAN)
        self.blinky = Player("Blinky", self, GHOST_SPAWN[0], GHOST, 0, GHOSTCOLOR[0])
        self.inky = Player("Inky", self, GHOST_SPAWN[1], GHOST, 1, GHOSTCOLOR[1])
        self.pinky = Player("Pinky", self, GHOST_SPAWN[2], GHOST, 2, GHOSTCOLOR[2])
        self.clyde = Player("Clyde", self, GHOST_SPAWN[3], GHOST, 3, GHOSTCOLOR[3])
        self.blinkyAI = AiEngine(self.blinky, self.pacman)
        self.inkyAI = AiEngine(self.inky, self.pacman, self.blinky)
        self.pinkyAI = AiEngine(self.pinky, self.pacman)
        self.clydeAI = AiEngine(self.clyde, self.pacman)

        self.blinkyAI.enableGhost()
        # self.inkyAI.enableGhost()
        # self.pinkyAI.enableGhost()
        # self.clydeAI.enableGhost()

############################ HELPER METHODS ##################################

    def __updateState(self, nextState):
        """Updates Current State and debugs it"""
        self.state = nextState
        debug("*State Updated to: " + nextState)

    def __renderGrid(self):
        """Renders Grid as well as colours the movable tiles"""
        if not OVERLAY_ENABLED:
            return
        for x in range(0, MAZE_WIDTH, TILESIZE):
            for y in range(0, MAZE_HEIGHT, TILESIZE):
                match GAMEBOARD[y//TILESIZE][x//TILESIZE]:
                    case 3:
                        self.overlay.set_alpha(50)
                        self.overlay.fill(PINK)
                    case 2:
                        self.overlay.set_alpha(50)
                        self.overlay.fill(YELLOW)
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

    def __renderText(self, text, screen, pos, colour, center=False):
        """Draws text onto the screen"""
        string = self.font.render(text, False, colour)
        stringSize = string.get_size()
        if pos[0] < 0:
            pos[0] = WINDOW_WIDTH+pos[0]-stringSize[0]
        if pos[1] < 0:
            pos[1] = WINDOW_HEIGHT+pos[1]-stringSize[1]
        if center:
            pos = [pos[0]-stringSize[0]//2, pos[1]-stringSize[1]//2]
        screen.blit(string, pos)

########################### UPDATE METHODS ####################################

    def __checkEvents(self):
        """Constantly checks for any event updates"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        self.pacman.queueMovement(1)
                    case pygame.K_a | pygame.K_LEFT:
                        self.pacman.queueMovement(2)
                    case pygame.K_s | pygame.K_DOWN:
                        self.pacman.queueMovement(3)
                    case pygame.K_d | pygame.K_RIGHT:
                        self.pacman.queueMovement(4)
                    case pygame.K_q:
                        self.running = False
                    case pygame.K_e:
                        pass
                    case pygame.K_r:
                        self.__updateState("play")
                        self.pacman.reset()
                        self.blinkyAI.reset()
                        self.inkyAI.reset()
                        self.pinkyAI.reset()
                        self.clydeAI.reset()

    def __renderGame(self):
        """Updates the Screen"""
        movementDict = {0: "NONE ", 1: "UP   ", 2: "LEFT ", 3: "DOWN ", 4: "RIGHT"}
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (PADDING, PADDING))
        self.__renderGrid()
        self.pacman.render()
        self.blinky.render()
        self.inky.render()
        self.pinky.render()
        self.clyde.render()
        renderFix = pygame.Surface((TILESIZE, TILESIZE))
        self.screen.blit(renderFix, (0, WINDOW_HEIGHT//2-3*TILESIZE//2))
        self.screen.blit(renderFix, (WINDOW_WIDTH-TILESIZE, WINDOW_HEIGHT//2-3*TILESIZE//2))
        self.__renderText("NEXT MOVEMENT: "+movementDict[self.pacman.nextMovement], self.screen, [-PADDING, -PADDING//4], RED)
        pygame.display.update()

    def __renderEnd(self):
        """Shows The Game Over Screen"""
        self.screen.fill(BLACK)
        self.__renderText("GAME OVER", self.screen, [WINDOW_WIDTH//2, WINDOW_HEIGHT//2], RED, True)
        pygame.display.update()

    def __tick(self):
        """Ran every tick"""
        self.pacman.tick()
        self.blinkyAI.tick()
        self.inkyAI.tick()
        self.pinkyAI.tick()
        self.clydeAI.tick()
        self.__renderGame()
        if self.blinkyAI.endCond() | self.inkyAI.endCond() | self.pinkyAI.endCond() | self.clydeAI.endCond():
            self.state = "gameover"

    def run(self):
        """Main Run sequence, runs everything"""
        debug("--Game Started--")
        while self.running:
            if self.state == "startup":
                self.__renderGame()
                self.__updateState("play")
                debug("--Start Sequence Initialized, Entering Play--")
            elif self.state == "play":
                self.__checkEvents()
                self.__tick()
            elif self.state == "gameover":
                self.__checkEvents()
                self.__renderEnd()
            self.clock.tick(FPS)
            pygame.display.update()
        pygame.quit()
        sys.exit()

##########################################################################
############################ MAIN SEQUENCE ###############################
##########################################################################


def main():
    Pac = Game()
    Pac.run()


if __name__ == "__main__":
    main()
