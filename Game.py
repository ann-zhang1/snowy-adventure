import pygame
import shelve
import math, random
from pygamegame import PygameGame
from MainCharacter import MainCharacter
from Map import Map
from Tree import Tree
from Rock import Rock
from Button import Button

# all fonts from fontsquirrel.com
# Seaside.ttf property of Nick's Fonts

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

        self.trees = pygame.sprite.Group()
        self.mainCharacter = MainCharacter(-1, -1, self)

        self.loadButtons()
        self.loadGame()
        self.restartGame()

    def loadButtons(self):
        left = self.width/9
        right = 8*self.width/9
        top = self.height/9
        bottom = 8*self.height/9

        # initialize all buttons
        self.mapCreationButtons = pygame.sprite.Group()
        self.saveMapButton = Button(left, bottom, 'Save Map')
        self.discardMapButton = Button(right, bottom, 'Discard Map')
        self.newMapButton = Button(right, top, 'New Map')
        self.returnButton = Button(left, top, 'Back')
        self.mapCreationButtons.add(self.saveMapButton)
        self.mapCreationButtons.add(self.discardMapButton)
        self.mapCreationButtons.add(self.newMapButton)
        self.mapCreationButtons.add(self.returnButton)

        self.startScreenButtons = pygame.sprite.Group()
        self.saveGameButton = Button(right, bottom, 'Save Game')
        self.mapModeButton = Button(self.width/2, self.height/3, 'Map Creation Mode')
        self.endlessMapButton = Button(self.width/2, 2*self.height/3, 'Endless Terrain Mode')
        # self.mapModeButton = Button(left, bottom, 'Maps')
        self.startScreenButtons.add(self.saveGameButton)
        self.startScreenButtons.add(self.mapModeButton)
        self.startScreenButtons.add(self.endlessMapButton)

        self.mapListButtons = pygame.sprite.Group()
        self.createButton = Button(right, top, 'Create')
        self.homeButton = Button(left, top, 'Back')
        self.mapListButtons.add(self.createButton)
        self.mapListButtons.add(self.homeButton)

        self.mapListButtonX = self.width/3
        self.mapListButtonY = self.height/4

    def restartGame(self):
        # always start in start screen mode
        print('len', len(Game.maps))
        self.startScreenMode = True
        self.mapListMode = False
        self.mapCreationMode = False
        self.helpScreenMode = False
        self.gameMode = False
        self.endlessMapMode = False

        # self.scrolling = False
        self.rotateAngle = 0

        self.recordName = False
        self.name = ''

        self.isGameOver = False

        self.isPaused = True
        self.waitingForFirstKeyPress = True
        # later, currMap will be initialized to original map instead of None
        self.currMap = None
        # initialize main character to be in center
        self.mainCharacter.reset()

        self.scrollingLeft = False
        self.scrollingRight = False
        self.scrollingUp = False
        self.scrollingDown = False

        self.distance = 0
        self.score = 0
        self.gameScroll = 0
        self.mapCreationScroll = 0
        self.mapListScroll = 0
        self.playerScroll = 0

        self.slopeAngle = 0

        self.theta = 0
        self.g = 1

        self.parabolaSign = 1
        self.cosDir = 1
        self.endlessMap = Map()
        self.loadEndlessMap()

    def loadEndlessMap(self, xParameter=1000):
        startY = random.randint(200, 350)
        for x in range(100, 106, 5):
            self.endlessMap.line += [(x, startY)]
        self.mainCharacter.cx, self.mainCharacter.cy = self.endlessMap.line[0]
        self.mainCharacter.cy -= self.mainCharacter.height
        self.extendEndlessMapCos(xParameter)
        self.const = 0.5 * self.mainCharacter.velX**2 + self.g*self.endlessMap.line[0][1]
        self.trees = pygame.sprite.Group()
        i = 0
        while i < len(self.endlessMap.line):
            x, y = self.endlessMap.line[i]
            self.trees.add(Tree(x, y))
            i += random.randint(75, 150)

    def extendEndlessMap(self, xParameter):
        mapX = self.endlessMap.line[-1][0]
        previousLen = len(self.endlessMap.line)
        # load endless map
        while mapX < xParameter:
            # generate a parabola
            previousY = self.endlessMap.line[-1][1]
            width = random.randint(300, 500)
            if self.parabolaSign == -1:
                height = random.randint(25, 75)
            else:
                height = random.randint(200, 350)
            # extent = random.randint(100, int(2*width/3))
            a = height/(width/2)**2
            if self.parabolaSign == -1:
                for x in range(0, int(width/2) + 5, 5):
                    yValue = -1*(a*(x-width/2)**2) + height
                    self.endlessMap.line += [(mapX + x, previousY + yValue)]
                lastX, lastY = self.endlessMap.line[-1]
                for x in range(0, 100, 5):
                    yValue = -1*(a*(x-100/2)**2) + 100
                    self.endlessMap.line += [(lastX + x, lastY + yValue - 100)]
                mapX += width/2 + 100
            else:
                for x in range(0, width + 5, 5):
                    yValue = -1*(a*(x-width/2)**2) - height
                    self.endlessMap.line += [(mapX + x, previousY - yValue - height*2)]
                mapX += width
            self.parabolaSign *= -1
        for i in range(previousLen, len(self.endlessMap.line)):
            if random.randint(0, 100) % 100 == 0:
                x, y = self.endlessMap.line[i]
                self.trees.add(Tree(x, y))
        while self.endlessMap.line[0][0] < self.endlessMap.line[-1][0] - 5000:
            self.endlessMap.line.pop(0)
    
    def extendEndlessMapCos(self, xParameter):
        mapX = self.endlessMap.line[-1][0]
        previousLen = len(self.endlessMap.line)
        # load endless map
        while mapX < xParameter:
            previousY = self.endlessMap.line[-1][1]
            width = random.randint(300, 600)
            if self.cosDir == -1:
                height = random.randint(75, 150)
                for x in range(0, width + 5, 5):
                    yValue = math.cos(x*math.pi/width)
                    self.endlessMap.line += [(mapX + x, previousY - yValue*height + height)]
            else:
                height = random.randint(25, 50)
                for x in range(0, width + 5, 5):
                    yValue = math.cos(x*math.pi/width + math.pi)
                    self.endlessMap.line += [(mapX + x, previousY - yValue*height - height)]
            self.cosDir *= -1
            mapX += width
        i = previousLen + 75
        while i < len(self.endlessMap.line):
            x, y = self.endlessMap.line[i]
            self.trees.add(Tree(x, y))
            i += random.randint(75, 150)
        while self.endlessMap.line[0][0] < self.endlessMap.line[-1][0] - 5000:
            self.endlessMap.line.pop(0)

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
            self.mapListButtons.add(Button(self.mapListButtonX, self.mapListButtonY, myMap.name))
            self.mapListButtonX += self.width/3
            if self.mapListButtonX >= self.width:
                self.mapListButtonX = self.width/3
                self.mapListButtonY += self.height/4

    def keyPressed(self, keyCode, modifier, event):
        if self.mapCreationMode:
            if keyCode == pygame.K_LEFT:
                self.scrollingLeft = True
            elif keyCode == pygame.K_RIGHT:
                self.scrollingRight = True
            if self.recordName:
                if keyCode == pygame.K_RETURN:
                    Game.maps[-1].name = self.name
                    self.mapListButtons.add(Button(self.mapListButtonX, self.mapListButtonY, self.name))
                    self.mapListButtonX += self.width/3
                    if self.mapListButtonX >= self.width:
                        self.mapListButtonX = self.width/3
                        self.mapListButtonY += self.height/4
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
            if keyCode == pygame.K_UP:
                self.scrollingUp = True
            # scroll right
            elif keyCode == pygame.K_DOWN:
                self.scrollingDown = True

        # if in game mode, press space to jump
        # if in game mode, press p to pause and unpause
        # press r to restart game in game mode
        elif self.gameMode or self.endlessMapMode:
            if self.waitingForFirstKeyPress:
                if keyCode == pygame.K_SPACE:
                    self.isPaused = False
                    self.waitingForFirstKeyPress = False
            elif keyCode == pygame.K_p:
                self.isPaused = not self.isPaused
            elif keyCode == pygame.K_r:
                self.restartGame()
            elif keyCode == pygame.K_UP and self.mainCharacter.canRotate:
                self.mainCharacter.isRotating = True
            elif keyCode == pygame.K_q:
                self.isGameOver = True
                self.gameMode = False
                self.endlessMapMode = False
                self.loadEndlessMap()
            else:
                if keyCode == pygame.K_SPACE and not self.isPaused and self.mainCharacter.canJump:
                    self.mainCharacter.jump()
                    self.mainCharacter.canRotate = True
        else:
            if keyCode == pygame.K_r:
                self.restartGame()

        # in any mode, press h to enter and exit the help screen mode
        # this will pause the current game if in gameplay
        if keyCode == pygame.K_h:
            self.helpScreenMode = not self.helpScreenMode
            self.isPaused = self.helpScreenMode
    
    def keyReleased(self, keyCode, modifier):
        if self.mapCreationMode:
            if keyCode == pygame.K_LEFT:
                self.scrollingLeft = False
            elif keyCode == pygame.K_RIGHT:
                    self.scrollingRight = False

        if self.mapListMode:
            if keyCode == pygame.K_UP or keyCode == pygame.K_DOWN:
                self.scrollingUp = False
                self.scrollingDown = False
                for button in self.mapListButtons:
                    if button.text != 'Create' and button.text != 'Home':
                        button.cy -= self.mapListScroll
                        button.update()

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
                self.mapCreationScroll = 0
                for button in self.mapCreationButtons:
                    if button.text == '':
                        button.cx = self.width/10
                        button.update()
            elif self.returnButton.clicked(x, y):
                self.mapCreationMode = False
                self.mapListMode = True
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
                        self.distance = 0
                for myMap in self.maps:
                    if myMap.name == self.currMap:
                        self.mainCharacter.cx, self.mainCharacter.cy = myMap.line[0]
                        self.mainCharacter.cy -= self.mainCharacter.height
                        self.trees = pygame.sprite.Group()
                        for i in range(len(myMap.line)):
                            if random.randint(0, 50) % 50 == 0:
                                x, y = myMap.line[i]
                                self.trees.add(Tree(x, y))
                        self.const = 0.5 * self.mainCharacter.velX**2 + self.g*myMap.line[0][1]
                if self.currMap != None:
                    self.startScreenMode = False
                    self.mapListMode = False
                    self.gameMode = True

                    self.mainCharacter.cy -= self.mainCharacter.height*3

        # if in game mode, hold the mouse to flip
        elif self.gameMode and not self.isPaused:
            pass

        # if save game button is clicked, call save game
        # if clicked on the map creation button, change modes
        elif self.startScreenMode:
            if self.saveGameButton.clicked(x, y):
                self.saveGame()
            elif self.mapModeButton.clicked(x, y):
                self.mapListMode = True
                self.startScreenMode = False
            elif self.endlessMapButton.clicked(x, y):
                self.endlessMapMode = True
                self.startScreenMode = False

    def mouseDrag(self, x, y):
        if self.mapCreationMode:
            # start creating a map
            if len(Game.maps) > 0:
                Game.maps[-1].line.append((x+self.mapCreationScroll, y))
            # can also switch to drag to draw a longer terrain

        # if in game mode, hold the mouse to flip
        elif self.gameMode and not self.isPaused:
            if self.mainCharacter.isRotating:
                self.mainCharacter.rotate(self.rotateAngle)
                self.rotateAngle += 45
                self.rotateAngle %= 360

    def mouseReleased(self, x, y):
        # self.scrolling = False
        self.mainCharacter.isRotating = False

    def timerFired(self, dt):
        if self.isGameOver:
            return
        # if in any of the other modes (i.e. help mode, paused, map, start),
        # then do nothing

        if self.mapCreationMode:
            if self.scrollingLeft:
                self.mapCreationScroll -= 5
            elif self.scrollingRight:
                self.mapCreationScroll += 5

        if self.mapListMode:
            if self.scrollingUp:
                self.mapListScroll = -5
            elif self.scrollingDown:
                self.mapListScroll = 5

        elif self.gameMode and not self.isPaused:
            # else, adjust position of player on line and move forward
            # later, currMap will be initialized to original map instead of None
            if self.currMap != None:
                for myMap in self.maps:
                    if myMap.name == self.currMap:
                        self.mainCharacter.velX = min(self.mainCharacter.velX, 30)
                        # if reached the end of the map, game over
                        if myMap.line[-1][0] <= self.mainCharacter.cx + 10:
                            self.isGameOver = True
                            self.gameMode = False
                            if self.distance > Game.bestDistance:
                                Game.bestDistance = self.distance
                            return

                        self.movePlayer(myMap)
        
        elif self.endlessMapMode and not self.isPaused:
            myMap = self.endlessMap
            self.mainCharacter.velX = min(self.mainCharacter.velX, 30)

            if myMap.line[-1][0] <= self.mainCharacter.cx + 10:
                self.isGameOver = True
                self.endlessMapMode = False
                self.loadEndlessMap()
                if self.distance > Game.bestDistance:
                    Game.bestDistance = self.distance
                return

            self.movePlayer(myMap)

            if self.mainCharacter.cx > self.endlessMap.line[-1][0]-self.width:
                self.extendEndlessMapCos(self.endlessMap.line[-1][0]+self.width)
        # update self.score and self.distance as playing

    def movePlayer(self, myMap):
        # find your current map
        # move the player
        y = self.mainCharacter.cy
        self.mainCharacter.cx += self.mainCharacter.velX
        self.gameScroll += self.mainCharacter.velX
        self.mainCharacter.cy += self.mainCharacter.velY

        self.distance = round(max(self.distance, self.mainCharacter.cx))

        # store original x to recenter when rotated
        x = self.mainCharacter.cx
        if self.findLeftRightPoints(myMap) == None:
            print('failed to find left right points')
            self.isGameOver = True
            self.gameMode = False
            self.endlessMapMode = False
            self.loadEndlessMap()
            return
        leftX, leftY, rightX, rightY = self.findLeftRightPoints(myMap)

        if rightX-leftX == 0: rightX += 0.1
        if rightY-leftY == 0: rightY += 0.1

        cy = self.findYAtX(leftX, leftY, rightX, rightY)
        x1, y2, x2, y2 = self.findImmediatePoints(myMap)
    
        # calculate angle to rotate player
        self.calculateAngle(leftX, leftY, rightX, rightY)
        if not self.mainCharacter.isRotating:
            self.mainCharacter.rotate(self.theta)
        
        if self.mainCharacter.isRotating:
            self.mainCharacter.rotate(self.rotateAngle)
            self.rotateAngle += 10
            self.rotateAngle %= 360

        # if im on the curve, attach to the curve
        if ((cy - self.mainCharacter.height <= self.mainCharacter.cy) and abs(x2-x1) < 25):
            # calculate acceleration on a slope
            thetaRadians = abs(self.theta * math.pi / 180)
            if self.theta > 0:
                thetaRadians *= -1
            accelX = self.g * math.cos(thetaRadians) * math.cos(math.pi/2 - thetaRadians)
            accelY = self.g * (math.sin(math.pi/2 - thetaRadians) * math.cos(thetaRadians) - 1)
            self.mainCharacter.velX += accelX
            self.mainCharacter.velY += accelY
            # bound to curve
            self.mainCharacter.cx = x
            self.mainCharacter.cy = cy - self.mainCharacter.height
            # adjust velocity
            self.mainCharacter.velY = (abs(-1 * self.mainCharacter.velX**2 + 2 * self.const - 2 * self.g * cy))**0.5
            self.mainCharacter.canJump = True

            if self.rotateAngle > 45 and self.rotateAngle < 315:
                print('failed jump')
                self.isGameOver = True
                self.gameMode = False
                self.endlessMapMode = False
                self.loadEndlessMap()
            
            self.mainCharacter.canRotate = False
            self.mainCharacter.isRotating = False
        else:
            self.mainCharacter.fall()
            self.mainCharacter.canJump = False

        if self.mainCharacter.cy > cy + self.mainCharacter.height + 10:
            print('below end of canvas')
            print(self.mainCharacter.cy, cy)
            self.isGameOver = True
            self.gameMode = False
            self.endlessMapMode = False
            self.loadEndlessMap()
            if self.distance > Game.bestDistance:
                Game.bestDistance = self.distance                           
        self.mainCharacter.update()

        self.playerScroll -= y - self.mainCharacter.cy

    def calculateAngle(self, leftX, leftY, rightX, rightY):
        slope = (rightY-leftY)/(rightX-leftX)
        slopeSign = slope/(abs(slope))
        absReciprocal = abs((rightX-leftX)/(rightY-leftY))
        self.theta = 180 / math.pi * math.atan(absReciprocal) - 90
        self.theta = slopeSign * self.theta

    def findLeftRightPoints(self, myMap):
        for i in range(len(myMap.line)):
            currX, currY = myMap.line[i]
            if currX > self.mainCharacter.cx:
                for j in range(10, -1, -1):
                    if 0 <= i+j < len(myMap.line):
                        rightX, rightY = myMap.line[i+j]
                        break
                for j in range(10, -1, -1):
                    if 0 <= i-j < len(myMap.line):
                        leftX, leftY = myMap.line[i-j]
                return leftX, leftY, rightX, rightY
    
    def findImmediatePoints(self, myMap):
        for i in range(len(myMap.line)):
            currX, currY = myMap.line[i]
            if currX > self.mainCharacter.cx:
                x2, y2 = currX, currY
                x1, y1 = myMap.line[i-1]
                return x1, y1, x2, y2
                
    def findYAtX(self, x1, y1, x2, y2):
        m = (y2-y1)/(x2-x1)
        b = y1 - m * x1
        return m * (self.mainCharacter.cx+self.mainCharacter.width/2) + b

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
        if i + 5 < len(myMap.line):
            x2, y2 = myMap.line[i+5]
        else:
            x2, y2 = myMap.line[i-5]
        return x1, y1, x2, y2
    
    def findClosestPointOnLine(self, x0, y0, x1, y1, x2, y2):
        a = y2 - y1
        b = x1 - x2
        c1 = a * x1 + b * y1
        c2 = -b * x0 + a * y0
        d = a**2 + b**2
        if d == 0:
            return x0, y0
        cx = (a * c1 - b * c2)/d
        cy = (a * c2 + b * c1)/d
        return cx, cy

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
        elif self.endlessMapMode:
            self.drawEndlessMap(screen)
        elif self.startScreenMode:
            self.drawStartScreen(screen)
        elif self.isGameOver:
            self.drawGameOver(screen)

        # otherwise, in game mode
        # draw game (foreground, background, terrain, weather, day)
        elif self.gameMode:
            self.drawGameMode(screen)

    def drawHelpScreen(self, screen):
        screen.fill((255,255,255))
        myfont = pygame.font.Font('Seaside.ttf', 20)
        line1 = myfont.render('HELP SCREEN', False, (0, 0, 0))
        line2 = myfont.render('In map list mode: use up down to scroll', False, (0, 0, 0))
        line3 = myfont.render('In map creation mode: use left down to scroll', False, (0, 0, 0))
        line4 = myfont.render('In game: space to jump, up to turn, q to give up', False, (0, 0, 0))
        line5 = myfont.render('PRESS H TO RETURN', False, (0, 0, 0))
        screen.blit(line1,(100, 150))
        screen.blit(line2,(100, 200))
        screen.blit(line3,(100, 250))
        screen.blit(line4,(100, 300))
        screen.blit(line5,(100, 350))

    def drawMapList(self, screen):
        # scroll using arrow keys (keyPressed)
        self.mapListButtons.draw(screen)
        self.drawButtonText(self.mapListButtons, screen)

    def drawMapCreation(self, screen):
        self.mapCreationButtons.draw(screen)
        self.drawButtonText(self.mapCreationButtons, screen)
        if len(Game.maps) > 0:
            Game.maps[-1].draw(screen, self.mapCreationScroll, self.playerScroll, self, False)
        if self.recordName:
            myfont = pygame.font.Font('Seaside.ttf', 30)
            line1 = myfont.render('Please enter a name for the map:', False, (48, 73, 12))
            screen.blit(line1,(100, 150))
        if self.name != '':
            myfont = pygame.font.Font('Seaside.ttf', 30)
            line1 = myfont.render(self.name, False, (48, 73, 12))
            screen.blit(line1,(100, 200))

    def drawStartScreen(self, screen):
        screen.fill((255,255,255))
        myfont = pygame.font.Font('Seaside.ttf', 30)
        line1 = myfont.render('WELCOME TO SNOWY ADVENTURE', False, (48, 73, 12))
        screen.blit(line1,(200, 50))

        self.startScreenButtons.draw(screen)
        self.drawButtonText(self.startScreenButtons, screen)
    
    def drawGameOver(self, screen):
        screen.fill((255,255,255))
        myfont = pygame.font.Font('Seaside.ttf', 30)
        line1 = myfont.render('GAME OVER', False, (48, 73, 12))
        line2 = myfont.render('PRESS R TO RESTART', False, (48, 73, 12))
        distance = 'DISTANCE: ' + str(self.distance)
        line3 = myfont.render(distance, False, (48, 73, 12))
        bestDistance=  'BEST DISTANCE: ' + str(Game.bestDistance)
        line4 = myfont.render(bestDistance, False, (48, 73, 12))
        screen.blit(line1,(100, 150))
        screen.blit(line2,(100, 250))
        screen.blit(line3,(100, 350))
        screen.blit(line4,(100, 450))
    
    def drawEndlessMap(self, screen):
        screen.fill((194,245,255))
        self.trees.draw(screen)
        self.endlessMap.draw(screen, self.gameScroll, self.playerScroll, self, True)
        for tree in self.trees:
            tree.fixX(self.gameScroll)
            tree.fixY(self.playerScroll)
            tree.update()
        screen.blit(self.mainCharacter.image, (self.mainCharacter.cx-self.gameScroll, self.mainCharacter.cy-self.playerScroll))

    
    def drawGameMode(self, screen):
        screen.fill((194,245,255))
        self.trees.draw(screen)
        if self.currMap == None:
            screen.fill((255,255,255))
            myfont = pygame.font.Font('Seaside.ttf', 25)
            line1 = myfont.render('NO MAP SELECTED; PRESS R', False, (0, 0, 0))
            line2 = myfont.render('GO TO THE MAPS PAGE TO CHOOSE/CREATE A MAP', False, (0, 0, 0))
            screen.blit(line1,(100, 150))
            screen.blit(line2,(100, 350))
        else:
            for myMap in self.maps:
                if myMap.name == self.currMap:
                    myMap.draw(screen, self.gameScroll, self.playerScroll, self, True)
                    # if self.mainCharacter.cx > myMap.line[-1][0] - self.width:
                    #    myMap.extend()
            for tree in self.trees:
                tree.fixX(self.gameScroll)
                tree.fixY(self.playerScroll)
                tree.update()
            screen.blit(self.mainCharacter.image, (self.mainCharacter.cx-self.gameScroll, self.mainCharacter.cy-self.playerScroll))

    def drawButtonText(self, buttonList, screen):
        for button in buttonList:
            myfont = pygame.font.Font('Antonio-Regular.ttf', 18)
            text = myfont.render(button.text, False, (0, 0, 0))
            text_rect = text.get_rect(center=(button.cx, button.cy))
            screen.blit(text, text_rect)
        
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