from cmu_graphics import *
from PIL import Image
import random
import time

def onAppStart(app):
    app.titleScreen = True
    app.titleURL = Image.open('generatedtext.jpg')
    app.titleImage = CMUImage(app.titleURL)
    app.startSelected = False
    app.loadSelected = False
    app.settingsSelected = False
    
    app.introCinematic = False
    app.introOpacity = 0
    app.introOpacitySlider = 100
    app.introOpacity1 = 0
    app.introOpacitySlider1 = 100
    app.introOpacity2 = 0
    app.introOpacitySlider2 = 100
    
    app.firstPrompt = False
    app.secondPrompt = False
    app.thirdPrompt = False

    app.moveRight = False
    app.moveLeft = False
    app.moveUp = False
    app.moveDown = False
    
    app.nodeX = 0
    app.nodeY = 0
    app.img = 'Player Character V6.png'

    app.enemies = []

    app.spells = []
    
    app.manaRegenRate = 10
    app.count = 0

    app.survival = False

    app.stepsPerSecond = 20


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
        drawLabel('START GAME', app.width//2, app.height//2 + app.height//10,
                    font = 'monospace', size = 30, fill = startColor)
        drawLabel('LOAD GAME', app.width//2, app.height//2 + (2 * app.height//10),
                    font = 'monospace', size = 30, fill = loadColor)
        drawLabel('SETTINGS', app.width//2, app.height//2 + (3 * app.height//10),
                    font = 'monospace', size = 30, fill = settingsColor)
    
    elif app.introCinematic == True:
        drawRect(0, 0, app.width, app.height, fill = 'black')
        if app.introOpacitySlider > -98:
            drawLabel('The world was destroyed in a matter of days', app.width//2, app.height//2,
                        fill = 'white', font = 'monospace', 
                        opacity = min(app.introOpacity, 100), size = 20)
        elif app.introOpacitySlider <= -98 and app.introOpacitySlider1 > -198:
            drawLabel('Only a few have survived till now to witness the horror of the aftermath',
                    app.width//2, app.height//2, fill = 'white', font = 'monospace',
                    opacity = min(app.introOpacity1, 100), size = 20)
        elif app.introOpacitySlider1 <= -98:
            drawLabel('You are among those few', app.width//2, app.height//2,
                    fill = 'white', font = 'monospace',
                    opacity = min(app.introOpacity2, 100), size = 20)
    
    if app.moveRight == True:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currScreen.drawScreen()
        wizard.drawHealthandMana()
        if app.survival == False:
            wizard.moveRight()
        else:
            if wizard.centerX >= app.width - 20:
                drawImage(CMUImage(Image.open(f'Player Character V6.png')),
                          wizard.centerX, wizard.centerY, align = 'center')
            else:
                wizard.moveRight()

    elif app.moveLeft == True:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currScreen.drawScreen()
        wizard.drawHealthandMana()
        if app.survival == False:
            wizard.moveLeft()
        else:
            if wizard.centerX <= 20:
                drawImage(CMUImage(Image.open(f'Player Character V7.png')),
                          wizard.centerX, wizard.centerY, align = 'center')
            else:
                wizard.moveLeft()
    
    elif app.moveUp == True:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currScreen.drawScreen()
        wizard.drawHealthandMana()
        if app.survival == False:
            wizard.moveUp()
        else:
            if wizard.centerY <= 20:
                drawImage(CMUImage(Image.open(f'PC Up Movement V0.png')),
                          wizard.centerX, wizard.centerY, align = 'center')
            else:
                wizard.moveUp()
    
    elif app.moveDown == True:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currScreen.drawScreen()
        wizard.drawHealthandMana()
        if app.survival == False:
            wizard.moveDown()
        else:
            if wizard.centerY >= app.height - 20:
                drawImage(CMUImage(Image.open(f'PC Down Movement V0.png')),
                          wizard.centerX, wizard.centerY, align = 'center')
            else:
                wizard.moveDown()
    
    elif app.thirdPrompt == None and app.introCinematic == False:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currScreen.drawScreen()
        wizard.drawHealthandMana()
        wizard.drawChar(app.img)
    
    for spell in app.spells:
        if spell.status == True:
            spell.drawProjectile(app.width, app.height, app.img)
    
    if app.survival == True:
        for enemy in app.enemies:
            if enemy.status == True and app.nodeX == 0 and app.nodeY == 0:
                enemy.spawnEnemy()
                enemy.displayHealth(enemy.stats[1])
                if enemy.stats[0] == 1:
                    #enemyAlg1(centerX, centerY, wizardCenterX, wizardCenterY)
                    enemyInteract = enemyAlg1(enemy.centerX, enemy.centerY, wizard.centerX, wizard.centerY)
                    if enemyInteract == True:
                        wizard.takeDamage(enemy.stats[2])
                    else:
                        enemy.centerX, enemy.centerY = enemyInteract
                for spell in app.spells:
                    enemy.checkProjectile(spell)
                    enemy.checkStatus()
        
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 30)
    
    if wizard.status == False:
        drawRect(0, 0, app.width, app.height, fill = 'black',)
        drawLabel('YOU DIED', app.width//2, app.height//2, fill = 'red', font = 'monospace')
    

    


def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

# def onMouseMove(app, mouseX, mouseY):
#     if screenDict == {}:
#         if distance(mouseX, mouseY, app.width//2, app.height//2 + app.height//10) <= 30: 
#             app.startSelected = True
#         else:
#             app.startSelected = False
#         if distance(mouseX, mouseY, app.width//2, app.height//2 + (2 * app.height//10)) <= 30: 
#             app.loadSelected = True
#         else:
#             app.loadSelected = False
#         if distance(mouseX, mouseY, app.width//2, app.height//2 + (3 * app.height//10)) <= 30:
#             app.settingsSelected = True
#         else:
#             app.settingsSelected = False

def onMousePress(app, mouseX, mouseY):
    if distance(mouseX, mouseY, app.width//2, app.height//2 + app.height//10) <= 30:
    #     app.titleScreen = False
    #     app.firstPrompt  = True
    #     app.introCinematic = True
    # if app.introCinematic == True:
        app.introCinematic = False
        app.thirdPrompt = None
    elif app.introCinematic == False and app.thirdPrompt == None:
        newFireball = Projectile('fireballI', 'Fireball I.png', 100, 
                       wizard.centerX, wizard.centerY, [20], True)
        app.spells.append(newFireball)
        if wizard.mana < newFireball.stats[0]:
            newFireball.status = False
        if newFireball.status == True and wizard.mana - newFireball.stats[0] <= 0:
            wizard.mana = 2
        elif newFireball.status == True:
            wizard.mana -= newFireball.stats[0]

def onStep(app):
    # if app.firstPrompt == True:
    #     app.introOpacity = 100 - abs(app.introOpacitySlider)
    #     if app.introOpacitySlider > -100:
    #         app.introOpacitySlider -= 1
    #     else:
    #         app.firstPrompt = False
    #         app.secondPrompt = True
    # if app.secondPrompt == True:
    #     app.introOpacity1 = 100 - abs(app.introOpacitySlider1)
    #     if app.introOpacitySlider1 > -100:
    #         app.introOpacitySlider1 -= 1
    #     else:
    #         app.secondPrompt = False
    #         app.thirdPrompt = True
    # if app.thirdPrompt == True:
    #     app.introOpacity2 = 100 - abs(app.introOpacitySlider2)
    #     if app.introOpacitySlider2 > -100:
    #         app.introOpacitySlider2 -= 1
    #     else:
    #         app.thirdPrompt = None
    # if app.thirdPrompt == None:
    #     app.introCinematic = False
    if app.moveRight == True:
        if wizard.centerX >= app.width:
            app.nodeX += 1
            wizard.centerX = 10
    if app.moveLeft == True:
        if wizard.centerX <= 0: 
            app.nodeX -= 1
            wizard.centerX = app.width - 10
    if app.moveUp == True:
        if wizard.centerY <= 0:
            app.nodeY += 1
            wizard.centerY = app.height - 10
    if app.moveDown == True:
        if wizard.centerY >= app.height:
            app.nodeY -= 1
            wizard.centerY = 10
    app.count += 1
    if app.count % app.manaRegenRate == 0:
        wizard.mana += 10
    for i in range(len(app.enemies)):
        if i >= len(app.enemies):
            break
        elif app.enemies[i].status == False:
            app.enemies.pop(i)
    for j in range(len(app.spells)):
        if j >= len(app.spells):
            break
        elif app.spells[j].status == False:
            app.spells.pop(j)
    
    

def onKeyPress(app, key):
    if key == 'd': 
        app.moveRight = True
    elif key == 'a':
        app.moveLeft = True
    elif key == 'w':
        app.moveUp = True
    elif key == 's':
        app.moveDown = True
    elif key == 'p':
        newDummy = Enemy('testDummy', 'Test Dummy.png', 512, 
                          random.randrange(0,app.width), random.randrange(0,app.height), 
                          [0, 8, 0], True)
        app.enemies.append(newDummy)
    elif key == 'l':
        newEvilDummy = Enemy('evilDummy', 'Evil Dummy.png', 256,
                             random.randrange(0,app.width), random.randrange(0,app.height),
                             [1, 4, 100], True)
        app.enemies.append(newEvilDummy)
    elif key == 't':
        app.survival = not app.survival
        app.enemies = []
    elif key == 'r':
        wizard.status = True
        wizard.centerX = app.width//2
        wizard.centerY = app.height//2
        wizard.health = 1000
        wizard.mana = 200



def onKeyRelease(app, key):
    if key == 'd':
        app.img = 'Player Character V6.png'
        app.moveRight = False
    elif key == 'a':
        app.img = 'Player Character V7.png'
        app.moveLeft = False
    elif key == 'w':
        app.img = 'PC Up Movement V0.png'
        app.moveUp = False
    elif key == 's':
        app.img = 'PC Down Movement V0.png'
        app.moveDown = False


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
        if self.nodeX == 0 and self.nodeY == 0:
            drawRect(0, 0, self.dimX, self.dimY, fill = 'green')
            drawImage(CMUImage(Image.open('Blackstone Fortress.png')), 
                      self.dimX//2, self.dimY//2, align = 'center')
            drawImage(CMUImage(Image.open('Spellbook Table.png')), 
                      self.dimX//2 - 150, self.dimY//2 + 100, align = 'center')
            drawImage(CMUImage(Image.open('Workshop.png')),
                      self.dimX//2, self.dimY//2 - 50, align = 'center')
            drawImage(CMUImage(Image.open('Portal.png')),
                      self.dimX//2, self.dimY//2 + 100, align = 'center')
            drawCircle(self.dimX//2 + 150, self.dimY//2 + 100, 32, fill = None, border = 'white',
                       borderWidth = 10)
            drawStar(self.dimX//2 + 150, self.dimY//2 + 100, 32, 4, fill = None, border = 'white',
                     borderWidth = 5)
            return             
        elif (self.nodeX, self.nodeY) in screenDict:
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
                if num < 3:
                    color = 'red'
                elif num < 10:
                    color = 'blue'
                elif num < 50:
                    color = 'lightGreen'
                elif num < 99:
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
        self.upCount = 1
        self.downCount = 1

        self.health = 1000
        self.mana = 200

        self.status = True
    
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
    
    def moveUp(self):
        self.centerY -= 10
        drawImage(CMUImage(Image.open(f'PC Up Movement V{self.upCount}.png')),
                  self.centerX, self.centerY, align = 'center')
        self.upCount += 1
        self.upCount %= 4
    
    def moveDown(self):
        self.centerY += 10
        drawImage(CMUImage(Image.open(f'PC Down Movement V{self.downCount}.png')),
                  self.centerX, self.centerY, align = 'center')
        self.downCount += 1
        self.downCount %= 4
    
    def drawChar(self, img):
        charURL = Image.open(img)
        charImage = CMUImage(charURL)
        drawImage(charImage, self.centerX, self.centerY, align = 'center')
    
    def drawHealthandMana(self):
        drawRect(20, 20, 210, 30, fill = None, border = 'saddleBrown', borderWidth = 5)
        drawRect(25, 25, max((self.health // 10) * 2, 2), 20, fill = 'crimson')
        drawRect(20, 60, 110, 30, fill = None, border = 'saddleBrown', borderWidth = 5)
        drawRect(25, 65, min((self.mana //2), 100), 20, fill = 'mediumBlue')
    
    def takeDamage(self, damage):
        if self.health - damage <= 2:
            self.health = 2
            self.status = False
        else:
            self.health -= damage
        

class Projectile:
    def __init__(self, name, img, rawDamage, startX, startY, stats, status):
        self.name = name
        self.img = img
        self.rawDamage = rawDamage
        self.centerX = startX
        self.centerY = startY
        self.stats = stats
        self.status = status
    
    def drawProjectile(self, dimX, dimY, orientation):
        drawImage(CMUImage(Image.open(f'{self.img}')), 
                    self.centerX, self.centerY, align = 'center')
        if orientation == 'Player Character V6.png':
            self.centerX += 30
        elif orientation == 'Player Character V7.png':
            self.centerX -= 30
        elif orientation == 'PC Up Movement V0.png':
            self.centerY -= 30
        elif orientation == 'PC Down Movement V0.png':
            self.centerY += 30
        if (self.centerX < 0 or self.centerX > dimX or
            self.centerY < 0 or self.centerY > dimY):
                self.status = False

class Enemy:
    def __init__(self, name, img, health, startX, startY, stats, status):
        self.name = name
        self.img = img
        self.health = health
        self.centerX = startX
        self.centerY = startY
        self.stats = stats
        self.status = status
    
    def spawnEnemy(self):
        drawImage(CMUImage(Image.open(self.img)), self.centerX, self.centerY, align = 'center')
    
    def checkProjectile(self, projectile):
        if distance(self.centerX, self.centerY, projectile.centerX, projectile.centerY) <= 64:
            self.takeDamage(projectile)
            projectile.status = False

    def takeDamage(self, projectile):
        self.health = max(2, self.health - projectile.rawDamage)
        projectile.centerX = -50
        projectile.centerY = -50
    
    def displayHealth(self, hfactor):
        drawRect(self.centerX, self.centerY - 64, 74, 20, fill = None, border = 'saddleBrown',
                 borderWidth = 5, align = 'center')
        drawRect(self.centerX + 0, self.centerY - 64, max(2, self.health // hfactor), 10, fill = 'crimson', align = 'center')
    
    def checkStatus(self):
        if self.health <= 2:
            self.status = False

def enemyAlg1(centerX, centerY, wizardCenterX, wizardCenterY):
    initialDistance = distance(centerX, centerY, wizardCenterX, wizardCenterY)
    if initialDistance <= 64:
        #TODO: Make better Damage cooldown timer that does not stop game momentarily
        endTime = time.time() + 0.5
        while time.time() < endTime:
            pass
        return True
    if centerX < wizardCenterX and centerY < wizardCenterY:
        centerX += int(((5 ** 2) * 0.5) ** 0.5)
        centerY += int(((5 ** 2) * 0.5) ** 0.5)
    if centerX < wizardCenterX and centerY > wizardCenterY:
        centerX += int(((5 ** 2) * 0.5) ** 0.5)
        centerY -= int(((5 ** 2) * 0.5) ** 0.5)
    if centerX > wizardCenterX and centerY > wizardCenterY:
        centerX -= int(((5 ** 2) * 0.5) ** 0.5)
        centerY -= int(((5 ** 2) * 0.5) ** 0.5)
    if centerX > wizardCenterX and centerY < wizardCenterY:
        centerX -= int(((5 ** 2) * 0.5) ** 0.5)
        centerY += int(((5 ** 2) * 0.5) ** 0.5)
    if centerX < wizardCenterX and centerY == wizardCenterY:
        centerX += 3
    if centerX > wizardCenterX and centerY == wizardCenterY:
        centerX -= 3
    if centerX == wizardCenterX and centerY < wizardCenterY:
        centerY += 3
    if centerX == wizardCenterX and centerY > wizardCenterY:
        centerY -= 3
    return centerX, centerY
    
    
    


wizard = Character(app.width//2, app.height//2)


    


def main():
    runApp()

main()