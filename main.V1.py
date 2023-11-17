from cmu_graphics import *
from PIL import Image
import random

def onAppStart(app):
    app.titleScreen = True
    app.titleURL = Image.open('generatedtext.jpg')
    app.titleImage = CMUImage(app.titleURL)
    app.startSelected = False
    app.loadSelected = False
    app.settingsSelected = False
    
    app.introCinematic = False
    app.introOpacity = 0
    app.introOpacitySlider = 200
    app.introOpacity1 = 0
    app.introOpacitySlider1 = 200
    app.introOpacity2 = 0
    app.introOpacitySlider2 = 200
    
    app.firstPrompt = False
    app.secondPrompt = False
    app.thirdPrompt = False

    app.moveRight = False
    app.moveLeft = False
    
    app.nodeX = 0
    app.nodeY = 0
    app.img = 'Player Character V6.png'

    app.stepsPerSecond = 50

screenDict = dict()

def redrawAll(app):
    if app.titleScreen == True:
        startColor = 'white'
        loadColor = 'white'
        settingsColor = 'white'
        if app.startSelected == True:
                startColor = 'red'
        if app.loadSelected == True:
                loadColor = 'red'
        if app.settingsSelected == True:
                settingsColor = 'red'
        drawRect(0, 0, app.width, app.height, fill = 'black')
        drawImage(app.titleImage, app.width//2, app.height//4, align = 'center',
                     width = 3 * app.width//4, height = app.height//2)
        #drawLabel('Title', app.width//2, app.height//4, align = 'center', fill = 'white')
        drawLabel('START GAME', app.width//2, app.height//2 + app.height//10,
                    font = 'monospace', size = 30, fill = startColor)
        drawLabel('LOAD GAME', app.width//2, app.height//2 + (2 * app.height//10),
                    font = 'monospace', size = 30, fill = loadColor)
        drawLabel('SETTINGS', app.width//2, app.height//2 + (3 * app.height//10),
                    font = 'monospace', size = 30, fill = settingsColor)
    
    elif app.introCinematic == True:
        drawRect(0, 0, app.width, app.height, fill = 'black')
        if app.introOpacitySlider > -198:
            drawLabel('The world was destroyed in a matter of days', app.width//2, app.height//2,
                        fill = 'white', font = 'monospace', 
                        opacity = min(app.introOpacity//2, 100), size = 20)
        elif app.introOpacitySlider <= -198 and app.introOpacitySlider1 > -198:
            drawLabel('Only a few have survived till now to witness the horror of the aftermath',
                    app.width//2, app.height//2, fill = 'white', font = 'monospace',
                    opacity = min(app.introOpacity1//2, 100), size = 20)
        elif app.introOpacitySlider1 <= -198:
            drawLabel('You are among those few', app.width//2, app.height//2,
                    fill = 'white', font = 'monospace',
                    opacity = min(app.introOpacity2//2, 100), size = 20)
    
    elif app.moveRight == True:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currScreen.drawScreen()
        wizard.moveRight()

    elif app.moveLeft == True:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currScreen.drawScreen()
        wizard.moveLeft()
    
    elif app.thirdPrompt == None and app.introCinematic == False:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currScreen.drawScreen()
        wizard.drawChar(app.img)
    


def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

def onMouseMove(app, mouseX, mouseY):
    if distance(mouseX, mouseY, app.width//2, app.height//2 + app.height//10) <= 30: 
        app.startSelected = True
    else:
        app.startSelected = False
    if distance(mouseX, mouseY, app.width//2, app.height//2 + (2 * app.height//10)) <= 30: 
        app.loadSelected = True
    else:
        app.loadSelected = False
    if distance(mouseX, mouseY, app.width//2, app.height//2 + (3 * app.height//10)) <= 30:
        app.settingsSelected = True
    else:
        app.settingsSelected = False

def onMousePress(app, mouseX, mouseY):
    if distance(mouseX, mouseY, app.width//2, app.height//2 + app.height//10) <= 30:
        app.titleScreen = False
        app.firstPrompt  = True
        app.introCinematic = True 

def onStep(app):
    if app.firstPrompt == True:
        app.introOpacity = 200 - abs(app.introOpacitySlider)
        if app.introOpacitySlider > -200:
            app.introOpacitySlider -= 1
        else:
            app.firstPrompt = False
            app.secondPrompt = True
    if app.secondPrompt == True:
        app.introOpacity1 = 200 - abs(app.introOpacitySlider1)
        if app.introOpacitySlider1 > -200:
            app.introOpacitySlider1 -= 1
        else:
            app.secondPrompt = False
            app.thirdPrompt = True
    if app.thirdPrompt == True:
        app.introOpacity2 = 200 - abs(app.introOpacitySlider2)
        if app.introOpacitySlider2 > -200:
            app.introOpacitySlider2 -= 1
        else:
            app.thirdPrompt = None
    if app.thirdPrompt == None:
        app.introCinematic = False
    if app.moveRight == True:
        if wizard.centerX >= app.width:
            app.nodeX += 1
            wizard.centerX = 10
    if app.moveLeft == True:
        if wizard.centerX <= 0: 
            app.nodeX -= 1
            wizard.centerX = app.width - 10
    

def onKeyPress(app, key):
    if key == 'd': 
        app.moveRight = True
    elif key == 'a':
        app.moveLeft = True

def onKeyRelease(app, key):
    if key == 'd':
        app.img = 'Player Character V6.png'
        app.moveRight = False
    elif key == 'a':
        app.img = 'Player Character V7.png'
        app.moveLeft = False


class Screen:
    def __init__(self, dimX, dimY):
        self.dimX = dimX
        self.dimY = dimY
    
    def __eq__(self, other):
        return isinstance(other, Screen) and self.nodeX == other.nodeX and self.nodeY == other.nodeY
    
    def __hash__(self):
        return hash(str((self.nodeX, self.nodeY)))
    
    #def draw(self, nodeX, nodeY):
        #if (nodeX, nodeY) in app.screenDict

class smallScreen:
    def __init__(self, dimX, dimY, nodeX, nodeY):
        self.dimX = dimX
        self.dimY = dimY
        self.nodeX = nodeX
        self.nodeY = nodeY

    def drawScreen(self):
        if (self.nodeX, self.nodeY) in screenDict:
            for row in range((self.dimY // 40) + 1):
                for col in range((self.dimX // 40) + 1):
                    val = screenDict[(self.nodeX, self.nodeY)]
                    colorVal =  val[col + (row * ((self.dimX // 40) + 1))]
                    drawRect(col * 40, row * 40, 40, 40, fill = colorVal)
            return
        screenList = []
        for row in range((self.dimY // 40) + 1):
            for col in range((self.dimX // 40) + 1):
                num = random.randrange(0, 101)
                if num < 10:
                    color = 'blue'
                elif num < 50:
                    color = 'lightGreen'
                elif num < 90:
                    color = 'green'
                else:
                    color = 'gold'
                drawRect(col * 40, row * 40, 40, 40, fill = color)
                screenList.append(color)
        screenDict[(self.nodeX, self.nodeY)] = screenList

class Character:
    def __init__(self, startX, startY):
        self.centerX = startX
        self.centerY = startY
        self.rightCount = 1
        self.leftCount = 1
    
    def moveRight(self):
        self.centerX += 10
        drawImage(CMUImage(Image.open(f'Player Character Right Movement V{self.rightCount}.png')),
                  self.centerX, self.centerY, align = 'center')
        self.rightCount += 1
        self.rightCount %= 4
    
    def moveLeft(self):
        self.centerX -= 10
        drawImage(CMUImage(Image.open(f'Player Character Left Movement V{self.leftCount}.png')),
                  self.centerX, self.centerY, align = 'center')
        self.leftCount += 1
        self.leftCount %= 4
    
    def drawChar(self,img):
        charURL = Image.open(img)
        charImage = CMUImage(charURL)
        drawImage(charImage, self.centerX, self.centerY, align = 'center')

wizard = Character(app.width//2, app.height//2)





    


def main():
    runApp()

main()