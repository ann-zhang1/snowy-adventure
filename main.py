import pygame
from pygamegame import PygameGame
from MainCharacter import MainCharacter
from Map import Map

class Game(PygameGame):
    maps = []

    def init(self):
        MainCharacter.init()
        Tree.init()
        self.loadGame()

    def restartGame(self):
        # always start in start screen mode
        startScreenMode = True
        mapCreationMode = False
        helpScreenMode = False
        currMap = None
    
    def loadGame(self):
        # load the game
        pass

    def keyPressed(self, keyCode, modifier):
        # if in start screen mode, press space to start the game

        # if in game mode, press space to jump

        # if in game mode, press p to pause and unpause

        # in any mode, press h to enter and exit the help screen mode
        # this will pause the current game if in gameplay
        pass

    def mousePressed(self, x, y):
        # if in game mode, hold the mouse to flip
        # if clicked on the map creation button, change modes

        if mapCreationMode:
            # start creating a map
            # make a new Map object, and add to self.ma
            pass

            # if save map button is clicked, then return to start screen
            # else if discard map button is saved, pop off of list

        # if save game button is clicked, call save game
        pass

    def mouseDrag(self, x, y):
        # if in game mode, hold the mouse to flip

        if mapCreationMode:
            # start creating a map
            # can also switch to drag to draw a longer terrain
            pass
        pass

    def mouseReleased(self, x, y):
        # finish updating map objects (do nothing?)

        # is there anything to do in mouse released?
        pass

    def timerFired(self, dt):
        # adjust fps as necessary

        # if in any of the other modes (i.e. help mode, paused, map, start),
        # then do nothing

        # else, adjust position of player on line and move forward

        # adjust speed of player

        # check for player collisions with line
        pass

    def redrawAll(self, screen):
        # first, check mode
        # if in any of the other modes, draw said mode
        if helpScreenMode:
            self.drawHelpScreen(screen)
        elif mapCreationMode:
            self.drawMapCreation(screen)
        elif startScreenMode:
            self.drawStartScreen(screen)

        # otherwise, in game mode
        # draw game (foreground, background, terrain, weather, day)
        pass

    def drawHelpScreen(self, screen):
        pass

    def drawMapCreation(self, screen):
        pass

    def drawStartScreen(self, screen):
        pass

    def saveGame(self):
        # save the game
        pass

Game(1000, 600).run()