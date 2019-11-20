import pygame
import shelve
from pygamegame import PygameGame
from MainCharacter import MainCharacter
from Map import Map
from Tree import Tree

class Game(PygameGame):
    maps = []
    bestScore = 0
    bestDistance = 0

    def init(self):
        MainCharacter.init()
        Tree.init()
        self.loadGame()
        
        pygame.font.init()

        self.restartGame()

    def restartGame(self):
        # always start in start screen mode
        self.startScreenMode = True
        self.mapCreationMode = False
        self.helpScreenMode = False
        self.gameMode = False

        self.isPaused = False
        self.currMap = None

        self.distance = 0
        self.score = 0
    
    def loadGame(self):
        # load the game
        pass

    def keyPressed(self, keyCode, modifier):
        # if in start screen mode, press space to start the game
        if self.startScreenMode:
            if keyCode == pygame.K_SPACE:
                self.startScreenMode = False
                self.gameMode = True

        # if in game mode, press space to jump
        # if in game mode, press p to pause and unpause
        # press r to restart game in game mode
        elif self.gameMode:
            if keyCode == pygame.K_SPACE and not self.isPaused:
                pass
            elif keyCode == pygame.K_p:
                self.isPaused = not self.isPaused

        # in any mode, press h to enter and exit the help screen mode
        # this will pause the current game if in gameplay
        if keyCode == pygame.K_h:
            self.helpScreenMode = not self.helpScreenMode

    def mousePressed(self, x, y):

        if self.mapCreationMode:
            # start creating a map
            # make a new Map object, and add to Game.maps
            Game.maps.append(Map())

            # if save map button is clicked, then return to start screen
            # else if discard map button is saved, pop off of list
            if self.saveMapButtonClicked(x, y):
                self.startScreenMode = True
            elif self.discardMapButtonClicked(x, y):
                Game.maps.pop()
                self.startScreenMode = True
        # if in game mode, hold the mouse to flip
        elif self.gameMode and not self.isPaused:
            pass

        # if save game button is clicked, call save game
        # if clicked on the map creation button, change modes
        elif self.startScreenMode and self.saveGameButtonClicked(x, y):
            pass

    def saveMapButtonClicked(self, x, y):
        pass

    def discardMapButtonClicked(self, x, y):
        pass

    def saveGameButtonClicked(self, x, y):
        pass

    def mouseDrag(self, x, y):
        if self.mapCreationMode:
            # start creating a map
            Game.maps[-1].line.append(x, y)
            # can also switch to drag to draw a longer terrain

        # if in game mode, hold the mouse to flip
        elif self.gameMode and not self.isPaused:
            pass

    def mouseReleased(self, x, y):
        # finish updating map objects (do nothing?)

        # is there anything to do in mouse released?
        pass

    def timerFired(self, dt):
        # adjust fps as necessary

        # if in any of the other modes (i.e. help mode, paused, map, start),
        # then do nothing

        if self.gameMode and not self.isPaused:
            # else, adjust position of player on line and move forward

            # adjust speed of player

            # check for player collisions with line
            pass

        # update self.score and self.distance as playing

    def redrawAll(self, screen):
        # first, check mode
        # if in any of the other modes, draw said mode
        if self.helpScreenMode:
            self.drawHelpScreen(screen)
        elif self.mapCreationMode:
            self.drawMapCreation(screen)
        elif self.startScreenMode:
            self.drawStartScreen(screen)

        # otherwise, in game mode
        # draw game (foreground, background, terrain, weather, day)
        pass

    def drawHelpScreen(self, screen):
        screen.fill((255,255,255))
        myfont = pygame.font.Font('Seaside.ttf', 75)
        line1 = myfont.render('YOU LOSE', False, (48, 73, 12))
        line2 = myfont.render('PRESS R TO RESTART', False, (48, 73, 12))
        screen.blit(line1,(100, 150))
        screen.blit(line2,(100, 350))


    def drawMapCreation(self, screen):
        pass

    def drawStartScreen(self, screen):
        screen.fill((255,255,255))
        myfont = pygame.font.Font('Seaside.ttf', 75)
        line1 = myfont.render('YOU LOSE', False, (48, 73, 12))
        line2 = myfont.render('PRESS R TO RESTART', False, (48, 73, 12))
        screen.blit(line1,(100, 150))
        screen.blit(line2,(100, 350))

    def saveGame(self):
        # save the game
        shelfFile = shelve.open('save_adventure_file')
        shelfFile['maps'] = Game.maps
        shelfFile['bestScore'] = Game.bestScore
        shelfFile['bestDistance'] = Game.bestDistance
        shelfFile.close()

Game(1000, 600).run()