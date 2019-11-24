import pygame
import shelve
import math
from pygamegame import PygameGame
from MainCharacter import MainCharacter
from Map import Map
from Tree import Tree
from Rock import Rock
from Button import Button

class Game(PygameGame):
    maps = []
    bestScore = 0
    bestDistance = 0

    def init(self):
        MainCharacter.init()
        Tree.init()
        Rock.init()
        Button.init()
        
        pygame.font.init()

        self.mainCharacter = MainCharacter(-1, -1)

        left = self.width/10
        right = 9*self.width/10
        top = self.height/10
        bottom = 9*self.height/10

        # initialize all buttons
        self.mapCreationButtons = pygame.sprite.Group()
        self.saveMapButton = Button(left, bottom, 'Save Map')
        self.discardMapButton = Button(right, bottom, 'Discard Map')
        self.newMapButton = Button(right, top, 'New Map')
        self.mapCreationButtons.add(self.saveMapButton)
        self.mapCreationButtons.add(self.discardMapButton)
        self.mapCreationButtons.add(self.newMapButton)

        self.startScreenButtons = pygame.sprite.Group()
        self.saveGameButton = Button(right, bottom, 'Save Game')
        self.startScreenButtons.add(self.saveGameButton)
        self.mapModeButton = Button(left, bottom, 'Maps')
        self.startScreenButtons.add(self.mapModeButton)

        self.mapListButtons = pygame.sprite.Group()
        self.createButton = Button(right, top, 'Create')
        self.mapListButtons.add(self.createButton)
        self.homeButton = Button(left, top, 'Home')
        self.mapListButtons.add(self.homeButton)

        self.loadGame()
        self.restartGame()

    def restartGame(self):
        # always start in start screen mode
        print('len', len(Game.maps))
        self.startScreenMode = True
        self.mapListMode = False
        self.mapCreationMode = False
        self.helpScreenMode = False
        self.gameMode = False

        self.recordName = False
        self.name = ''

        self.isPaused = False
        # later, currMap will be initialized to original map instead of None
        self.currMap = None
        # initialize main character to be in center
        self.mainCharacter.cx, self.mainCharacter.cy = -1, -1

        self.distance = 0
        self.score = 0
        self.scrollX = 0
    
    # code based from 
    # https://inventwithpython.com/blog/2012/05/03/implement-a-save-game-feature-in-python-with-the-shelve-module/
    def loadGame(self):
        # load the game
        shelfFile = shelve.open('save_adventure_file')
        Game.maps = shelfFile['maps']
        Game.bestScore = shelfFile['bestScore']
        Game.bestDistance = shelfFile['bestDistance']
        shelfFile.close()
        for myMap in Game.maps:
            self.mapListButtons.add(Button(self.width/2, self.height/2, myMap.name))

    def keyPressed(self, keyCode, modifier, event):
        if self.mapCreationMode:
            if self.recordName:
                if keyCode == pygame.K_RETURN:
                    Game.maps[-1].name = self.name
                    self.mapListButtons.add(Button(self.width/2, self.height/2, self.name))
                    self.name = ''
                    self.mapCreationMode = False
                elif keyCode == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    self.name += event.unicode

        # if in map list mode, use left and right arrow keys to scroll
        # between different maps
        elif self.mapListMode:
            # scroll left
            if keyCode == pygame.K_LEFT:
                pass
            # scroll right
            elif keyCode == pygame.K_RIGHT:
                pass

        # if in start screen mode, press space to start the game
        elif self.startScreenMode:
            if keyCode == pygame.K_SPACE:
                self.startScreenMode = False
                self.gameMode = True

        # if in game mode, press space to jump
        # if in game mode, press p to pause and unpause
        # press r to restart game in game mode
        elif self.gameMode:
            if keyCode == pygame.K_SPACE and not self.isPaused:
                self.mainCharacter.isJumping = True
            elif keyCode == pygame.K_p:
                self.isPaused = not self.isPaused
            elif keyCode == pygame.K_r:
                self.restartGame()

        # in any mode, press h to enter and exit the help screen mode
        # this will pause the current game if in gameplay
        elif keyCode == pygame.K_h:
            self.helpScreenMode = not self.helpScreenMode
            self.isPaused = self.helpScreenMode

    def mousePressed(self, x, y):
        if self.mapCreationMode:
            # if save map button is clicked, then return to start screen
            # else if discard map button is saved, pop off of list
            if self.saveMapButton.clicked(x, y):
                # create a pop-up asking for the name of the map
                # set the name of the map
                # go back to the maps mode
                self.recordName = True
            elif self.discardMapButton.clicked(x, y):
                if len(Game.maps) > 0:
                    deleteMap = Game.maps.pop()
                    newButtons = pygame.sprite.Group()
                    for button in self.mapListButtons:
                        if button.text != deleteMap.name:
                            newButtons.add(button)
                    self.mapListButtons = newButtons
                self.mapCreationMode = False
                self.startScreenMode = True
            elif self.newMapButton.clicked(x,y):
                # start creating a map
                # make a new Map object, and add to Game.maps
                Game.maps.append(Map())

        elif self.mapListMode:
            if self.createButton.clicked(x, y):
                self.mapCreationMode = True
            elif self.homeButton.clicked(x, y):
                self.mapListMode = False
                self.startScreenMode = True
            else:
                for button in self.mapListButtons:
                    if button.clicked(x, y):
                        self.currMap = button.text
                for myMap in self.maps:
                    if myMap.name == self.currMap:
                        self.mainCharacter.cx, self.mainCharacter.cy = myMap.line[0]
                        self.mainCharacter.cx -= self.mainCharacter.width/2
                        self.mainCharacter.cy -= self.mainCharacter.height

        # if in game mode, hold the mouse to flip
        elif self.gameMode and not self.isPaused:
            pass

        # if save game button is clicked, call save game
        # if clicked on the map creation button, change modes
        elif self.startScreenMode:
            if self.saveGameButton.clicked(x, y):
                self.saveGame()
            if self.mapModeButton.clicked(x, y):
                self.mapListMode = True

    def mouseDrag(self, x, y):
        if self.mapCreationMode:
            # start creating a map
            if len(Game.maps) > 0:
                Game.maps[-1].line.append((x, y))
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
            # later, currMap will be initialized to original map instead of None
            if self.currMap != None:
                for myMap in self.maps:
                    if myMap.name == self.currMap:
                        # find your current map
                        # move the player
                        if self.mainCharacter.isJumping:
                            # move in a jumping fashion
                            pass
                        else:
                            x1, y1, x2, y2 = self.findTwoPoints(myMap)
                            print(f'x1 {x1} y1 {y1} x2 {x2} y2 {y2}')
                            self.mainCharacter.cy = y1 - self.mainCharacter.height
                            if x2-x1 == 0: x2 += 1
                            if y2-y1 == 0: y2 += 1
                            slope = (y2-y1)/(x2-x1)
                            slopeSign = slope/(abs(slope))
                            angle = 90 - 180 / math.pi * math.atan(abs(x2-x1)/abs(y2-y1))
                            rotateAngle = angle
                            print(f'rotateAngle {rotateAngle}')
                            self.mainCharacter.rotate(rotateAngle)
                            self.mainCharacter.cx += 5
                            self.scrollX += 5
            # adjust speed of player

            # check for player collisions with line
            pass

        # update self.score and self.distance as playing

    def findTwoPoints(self, myMap):
        characterPoint = self.mainCharacter.cx, self.mainCharacter.cy
        closestPoint = myMap.line[0]
        closestIndex = 0
        for i in range(len(myMap.line)):
            point = myMap.line[i]
            if self.calDistance(point, characterPoint) < self.calDistance(closestPoint, characterPoint):
                closestPoint = point
                closestIndex = i
        x1, y1 = closestPoint
        print(len(myMap.line))
        if i + 1 < len(myMap.line):
            x2, y2 = myMap.line[i+1]
        else:
            x2, y2 = myMap.line[i-1]
        return x1, y1, x2, y2

    def calDistance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x2-x1)**2 + (y2-y1)**2)**0.5

    def redrawAll(self, screen):
        # first, check mode
        # if in any of the other modes, draw said mode
        if self.helpScreenMode:
            self.drawHelpScreen(screen)
        elif self.mapCreationMode:
            self.drawMapCreation(screen)
        elif self.mapListMode:
            self.drawMapList(screen)
        elif self.startScreenMode:
            self.drawStartScreen(screen)

        # otherwise, in game mode
        # draw game (foreground, background, terrain, weather, day)
        elif self.gameMode:
            screen.blit(self.mainCharacter.image, (self.mainCharacter.cx-self.scrollX, self.mainCharacter.cy))
            for myMap in self.maps:
                if myMap.name == self.currMap:
                    myMap.draw(screen, self.scrollX)

    def drawHelpScreen(self, screen):
        screen.fill((255,255,255))
        myfont = pygame.font.Font('Seaside.ttf', 75)
        line1 = myfont.render('HELP SCREEN', False, (0, 0, 0))
        line2 = myfont.render('PRESS H TO RETURN', False, (0, 0, 0))
        screen.blit(line1,(100, 150))
        screen.blit(line2,(100, 350))

    def drawMapList(self, screen):
        # scroll using arrow keys (keyPressed)
        self.mapListButtons.draw(screen)
        self.drawButtonText(self.mapListButtons, screen)

    def drawMapCreation(self, screen):
        self.mapCreationButtons.draw(screen)
        self.drawButtonText(self.mapCreationButtons, screen)
        if len(Game.maps) > 0:
            Game.maps[-1].draw(screen)
        if self.name != '':
            myfont = pygame.font.Font('Seaside.ttf', 30)
            line1 = myfont.render(self.name, False, (48, 73, 12))
            screen.blit(line1,(100, 150))

    def drawStartScreen(self, screen):
        screen.fill((255,255,255))
        myfont = pygame.font.Font('Seaside.ttf', 30)
        line1 = myfont.render('WELCOME TO SNOWY ADVENTURE', False, (48, 73, 12))
        line2 = myfont.render('PRESS SPACE TO START', False, (48, 73, 12))
        screen.blit(line1,(100, 150))
        screen.blit(line2,(100, 350))

        self.startScreenButtons.draw(screen)
        self.drawButtonText(self.startScreenButtons, screen)
    
    def drawButtonText(self, buttonList, screen):
        for button in buttonList:
            myfont = pygame.font.Font('Antonio-Regular.ttf', 18)
            text = myfont.render(button.text, False, (0, 0, 0))
            screen.blit(text, (button.cx-button.width/3, button.cy-button.height/3))
        

    # code based from 
    # https://inventwithpython.com/blog/2012/05/03/implement-a-save-game-feature-in-python-with-the-shelve-module/
    def saveGame(self):
        # save the game
        shelfFile = shelve.open('save_adventure_file')
        shelfFile['maps'] = Game.maps
        shelfFile['bestScore'] = Game.bestScore
        shelfFile['bestDistance'] = Game.bestDistance
        shelfFile.close()

Game(1000, 600).run()