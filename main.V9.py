from cmu_graphics import *
from PIL import Image
import random
import time
import numpy as np
import sys


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

    app.inventory = dict()
    app.inventory[None] = 1
    
    app.manaRegenRate = 10
    app.count = 0

    app.PCSpellsUnlocked = {}
    app.enemiesUnlocked = []

    app.upgrade = False
    app.PCUpgradeInteract = False
    app.spellTable = False
    app.spellBooksCollected = [SpellBook("A Basic Spell Only Requiring A Little Ingenuity.", 
                                         'fireball', [(None, 0)], False, False)]
    app.spellBookSelected = False, -2
    app.bookshelf = False
    app.displayDecryptResTrue = False
    app.displayDecryptResFalse = False
    app.learnSpell = False
    app.lackMaterials = False
    app.lackNumMaterials = False

    app.workshop = False
    app.skillUpgrade = False

    app.survival = False

    app.invincible = False
    app.invincibleCounter = 0
    # app.dodgeCooldown = 0
    # app.canDodge = True

    #app.downtime = DowntimeCountdown()
    # print('starting')
    # app.downtime.start()

    app.totalCounter = 5 * 20
    app.roundNum = 1
    app.timerColor = 'blue'

    app.roundMax = 4
    app.win = False


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
        drawLabel(f'{app.totalCounter//(20 * 60)}m, {(app.totalCounter // 20) % 60}s',
                  app.width - 20, 20, align = 'right-top', 
                  font = 'monospace', size = 30, fill = app.timerColor)
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
        drawLabel(f'{app.totalCounter//(20 * 60)}m, {(app.totalCounter // 20) % 60}s',
                  app.width - 20, 20, align = 'right-top', 
                  font = 'monospace', size = 30, fill = app.timerColor)
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
        drawLabel(f'{app.totalCounter//(20 * 60)}m, {(app.totalCounter // 20) % 60}s',
                  app.width - 20, 20, align = 'right-top', 
                  font = 'monospace', size = 30, fill = app.timerColor)
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
        drawLabel(f'{app.totalCounter//(20 * 60)}m, {(app.totalCounter // 20) % 60}s',
                  app.width - 20, 20, align = 'right-top', 
                  font = 'monospace', size = 30, fill = app.timerColor)
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
        drawLabel(f'{app.totalCounter//(20 * 60)}m, {(app.totalCounter // 20) % 60}s',
                  app.width - 20, 20, align = 'right-top', 
                  font = 'monospace', size = 30, fill = app.timerColor)
    #checkSpellTableInteraction  checkWorkshopInteraction checkCharUpgradeInteraction
    if wizard.checkSpellTableInteraction(app.width, app.height) and app.PCUpgradeInteract == True:
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 80)
        drawImage(CMUImage(Image.open('Upgrade Canvas.png')), 
                  app.width//2, app.height//2, align = 'center')
        
        a, b = app.spellBookSelected
        if a == True:
            drawImage(CMUImage(Image.open('Spellbook.png')), app.width//2, app.height//2,
                      align = 'center')
            for line in range(len(app.spellBooksCollected[b].scrambledText) // 26 + 1):
                drawLabel(app.spellBooksCollected[b].scrambledText[(line*26):(line*26) + 26], 
                        app.width//2 - 230, (app.height//2 - 210) + (line*20), 
                        fill = 'black', font = 'monospace', size = 12, bold = True, align = 'left-top')
            if app.displayDecryptResTrue == False and app.displayDecryptResFalse == False:
                drawRect(app.width//2 - 130, app.height//2 + 150, 200, 35,
                         fill = None, border = 'black', align = 'center')
                drawLabel('Decrypt', app.width//2 - 130, app.height//2 + 150, 
                            fill = 'black', font = 'monospace', bold = True, size = 30)
            elif app.displayDecryptResTrue == True:
                drawLabel('Success!', app.width//2 - 130, app.height//2 + 150,
                          fill = 'black', font = 'monospace', bold = True, size = 30)
                drawLabel('Required Materials', app.width//2 + 130, app.height//2 - 210,
                          fill = 'black', font = 'monospace', bold = True, size = 20)
                if app.learnSpell == True:
                    drawLabel('Spell Learned!', app.width//2 + 130, app.height//2 + 150,
                          fill = 'black', font = 'monospace', bold = True, size = 25)
                    drawLabel('Press esc to exit upgrade menu', 
                              app.width//2 + 130, app.height//2 + 100, 
                              fill = 'black', font = 'monospace', bold = True, size = 12)
                elif app.spellBooksCollected[b].reqMaterials == [(None, 0)]:
                    drawRect(app.width//2 + 130, app.height//2 + 150, 220, 35,
                         fill = None, border = 'black', align = 'center')
                    drawLabel('Learn Spell', app.width//2 + 130, app.height//2 + 150,
                          fill = 'black', font = 'monospace', bold = True, size = 30)
                    drawLabel('None', app.width//2 + 130, app.height//2 - 180,
                              fill = 'black', font = 'monospace', bold = True, size = 12)
                elif app.learnSpell == False:
                    drawRect(app.width//2 + 130, app.height//2 + 150, 220, 35,
                         fill = None, border = 'black', align = 'center')
                    drawLabel('Learn Spell', app.width//2 + 130, app.height//2 + 150,
                          fill = 'black', font = 'monospace', bold = True, size = 30)
                    for i in range(len(app.spellBooksCollected[b].reqMaterials)):
                        drawLabel((f'{app.spellBooksCollected[b].reqMaterials[i][1]}' + ' '
                                   f'{app.spellBooksCollected[b].reqMaterials[i][0]}'),
                                  app.width//2 + 130, (app.height//2 - 180) + (i * 20),
                                  fill = 'black', font = 'monospace', bold = True, size = 12)
            elif app.displayDecryptResFalse == True:
                drawRect(app.width//2 - 130, app.height//2 + 150, 200, 35, 
                         fill = None, border = 'black', align = 'center')
                drawLabel('Decrypt', app.width//2 - 130, app.height//2 + 150, 
                            fill = 'black', font = 'monospace', bold = True, size = 30)
                drawLabel('Try again', app.width//2 - 130, app.height//2 + 110,
                          fill = 'black', font = 'monospace', bold = True, size = 30)


        elif app.bookshelf == False:
            drawLabel('The SpellTable. The place for all your spell upgrade needs!', 
                    app.width//2, app.height//2 - 250,
                    fill = 'black', font = 'monospace', size = 20, bold = True)
            drawLabel('Activate and solve collected spellbooks to get new spells.',
                    app.width//2, app.height//2 - 230,
                    fill = 'black', font = 'monospace', size = 20, bold = True)
            drawLabel('View collected spellbooks in the bookshelf.',
                    app.width//2, app.height//2 - 210,
                    fill = 'black', font = 'monospace', size = 20, bold = True)
            drawImage(CMUImage(Image.open('Bookshelf.png')), 
                      app.width//2, app.height//2, align = 'center')
        
        elif app.bookshelf == True:
            for i in range(len(app.spellBooksCollected)):
                drawRect(app.width//2, (app.height//2 - 250) + (i* 20), 250, 20, 
                         fill = None, border = 'black', align = 'center')
                drawLabel(app.spellBooksCollected[i].spellUnlock, 
                          app.width//2, (app.height//2 - 250) + (i*20), 
                          font = 'monospace', size = 12, bold = True)
            
    if wizard.checkWorkshopInteraction(app.width, app.height) and app.PCUpgradeInteract == True:
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 80)
        drawImage(CMUImage(Image.open('Upgrade Canvas.png')),
                  app.width//2, app.height//2, align = 'center')
        drawLabel('The Workshop. The place for all your base upgrade needs!',
                  app.width//2, app.height//2 - 250, align = 'center',
                  fill = 'black', font = 'monospace', size = 12, bold = True)
    
    if wizard.checkCharUpgradeInteraction(app.width, app.height) and app.PCUpgradeInteract == True:
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 80)
        drawImage(CMUImage(Image.open('Upgrade Canvas.png')),
                  app.width//2, app.height//2, align = 'center')
        drawLabel('The Skill Tree. The place for all your character upgrade needs!',
                  app.width//2, app.height//2 - 250, align = 'center',
                  fill = 'black', font = 'monospace', size = 12, bold = True)
    
    for spell in app.spells:
        if spell.status == True:
            spell.drawProjectile(app.width, app.height, spell.stats[-1])
    
    if app.survival == True:
        for enemy in app.enemies:
            if enemy.status == True and app.nodeX == 0 and app.nodeY == 0:
                enemy.spawnEnemy()
                enemy.displayHealth(enemy.stats[1])
                if enemy.stats[0] == 1:
                    #enemyAlg1(centerX, centerY, wizardCenterX, wizardCenterY)
                    enemyInteract = enemy.enemyAlg1(enemy.centerX, enemy.centerY, wizard.centerX, wizard.centerY)
                    if enemyInteract == True:
                        wizard.takeDamage(enemy.stats[2])
                    else:
                        enemy.centerX, enemy.centerY = enemyInteract
                elif enemy.stats[0] == 2:
                    if enemy.stats[3] % 60 == 0:
                        enemyMovement = enemy.enemyAlg2(wizard.centerX, wizard.centerY, app.width, app.height)
                        enemyMovement.reverse()
                        for node in enemyMovement:
                            enemy.centerX, enemy.centerY = node[1] * 10, node[0] * 10
                            drawImage(CMUImage(Image.open(enemy.img)), node[1] * 10, node[0] * 10,
                                      align = 'center')
                        if enemy.interact() == True:
                            wizard.takeDamage(enemy.stats[2])
                for spell in app.spells:
                    enemy.checkProjectile(spell)
                    enemy.checkStatus()
        
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 30)
    
    if wizard.status == False:
        drawRect(0, 0, app.width, app.height, fill = 'black',)
        drawLabel('YOU DIED', app.width//2, app.height//2, fill = 'red', font = 'monospace')
    
    if app.win == True:
        drawRect(0, 0, app.width, app.height, fill = 'black')
        drawLabel('You Survived.', app.width//2, app.height//2, 
                  font = 'monospace', size = 30, fill = 'white')
        drawLabel('Thank you for playing!', app.width//2, app.height//2 + 50,
                  font = 'monospace', size = 30, fill = 'white')
        
    
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
        #app.win = True
        #endGame()
    elif app.introCinematic == False and app.thirdPrompt == None and app.upgrade == False:
        newFireball = Projectile('fireballI', 'Fireball I.png', 100, 
                       wizard.centerX, wizard.centerY, [20], True)
        newFireball.stats.append(app.img)
        app.spells.append(newFireball)
        if wizard.mana < newFireball.stats[0]:
            newFireball.status = False
        if newFireball.status == True and wizard.mana - newFireball.stats[0] <= 0:
            wizard.mana = 2
        elif newFireball.status == True:
            wizard.mana -= newFireball.stats[0]
    if app.survival == False:
        if (wizard.checkSpellTableInteraction(app.width, app.height) and app.PCUpgradeInteract == True
            and distance(mouseX, mouseY, app.width//2, app.height//2)):
                app.bookshelf = True
        if app.bookshelf == True and app.spellBookSelected[0] == False:
            for i in range(len(app.spellBooksCollected)):
                if distance(mouseX, mouseY, app.width//2, (app.height//2 - 250) + (i * 20)) <= 20:
                    app.spellBookSelected = True, i
                    app.spellBooksCollected[i].scrambledText = app.spellBooksCollected[i].activateSpellBook()
        if (app.bookshelf == True and app.spellBookSelected[0] == True 
            and distance(mouseX, mouseY, app.width//2 - 130, app.height//2 + 150) <= 30):
                decodeTextAttempt = app.getTextInput('Enter decrypted text here: ')
                if decodeTextAttempt == None:
                    decodeTextAttempt = app.getTextInput('Enter decrypted text here: ')
                print(app.spellBooksCollected[app.spellBookSelected[1]].checkSolveStatus(decodeTextAttempt))
                if app.spellBooksCollected[app.spellBookSelected[1]].checkSolveStatus(decodeTextAttempt) == False: 
                    app.displayDecryptResTrue = True
                else:
                    app.displayDecryptResFalse = True
        if (app.displayDecryptResTrue == True and
            distance(mouseX, mouseY, app.width//2 + 130, app.height//2 + 150) <= 40):
                for i in range(len(app.spellBooksCollected[app.spellBookSelected[1]].reqMaterials)):
                    currMaterial, numMaterial = app.spellBooksCollected[app.spellBookSelected[1]].reqMaterials[i]
                    if currMaterial in app.inventory:
                        if app.inventory[currMaterial] > numMaterial:
                            app.inventory[currMaterial] -= numMaterial
                            app.learnSpell = True
                            app.spellBooksCollected.pop(app.spellBookSelected[1])
                        elif app.inventory[currMaterial] == numMaterial:
                            del app.inventory[currMaterial]
                            app.learnSpell = True
                            app.spellBooksCollected.pop(app.spellBookSelected[1])
                        else:
                            app.lackNumMaterials = True
                    else:
                        app.lackMaterials = True
# def endGame():
#     print('cool')
#     app.paused = True
                
def onStep(app):
    for enemy in app.enemies:
        if enemy.name == 'demonSpirit':
            enemy.stats[3] += 1
    if app.thirdPrompt == None and app.introCinematic == False:
        app.totalCounter -= 1
    if app.totalCounter <= 0:
        if app.survival == True:
            app.enemies = []
            app.spells = []
            app.survival = False
            app.timerColor = 'blue'
            app.roundNum += 1
            if app.roundNum >= app.roundMax:
                app.win = True
                #endGame()
            print(app.roundNum)
            app.totalCounter = (10 * 20) #* app.roundNum
        elif app.survival == False:
            app.survival = True
            app.timerColor = 'red'
            app.totalCounter = (30 * 20)
    if app.survival == True:
        ranNum = random.randrange(0, 1000)
        if ranNum >= 998 and app.roundNum >= 3:
            newEnemy =  Enemy('demonSpirit', 'Demon Spirit.png', 128,
                                random.randrange(0, app.width), random.randrange(0, app.height),
                                [2, 2, 200, 1], True)
            app.enemies.append(newEnemy)
        elif ranNum >= 995 and app.roundNum >= 2:
            newEnemy = Enemy('evilDummy', 'Evil Dummy.png', 256,
                                random.randrange(0,app.width), random.randrange(0,app.height),
                                [1, 4, 100], True)
            app.enemies.append(newEnemy)
        elif ranNum >= 985 and app.roundNum >= 1:
            newEnemy =  Enemy('testDummy', 'Test Dummy.png', 64, 
                                random.randrange(0,app.width), random.randrange(0,app.height), 
                                [0, 1, 0], True)
            app.enemies.append(newEnemy)
    # app.invincibleCounter += 1
    # if app.invincibleCounter % 40 == 0:
    #         app.invincibleCounter = False
    # app.dodgeCooldown += 1
    # if app.dodgeCooldown % 50 == 0:
    #     app.canDodge = True
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
    if app.count % app.manaRegenRate == 0 and wizard.mana < 200:
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
    if app.upgrade == False:
        if key == 'd': 
            app.moveRight = True
        elif key == 'a':
            app.moveLeft = True
        elif key == 'w':
            app.moveUp = True
        elif key == 's':
            app.moveDown = True
    if key == 'p':
        newDummy = Enemy('testDummy', 'Test Dummy.png', 512, 
                          random.randrange(0,app.width), random.randrange(0,app.height), 
                          [0, 8, 0], True)
        app.enemies.append(newDummy)
    # if key == 'l':
    #     newEvilDummy = Enemy('evilDummy', 'Evil Dummy.png', 256,
    #                          random.randrange(0,app.width), random.randrange(0,app.height),
    #                          [1, 4, 100], True)
    #     app.enemies.append(newEvilDummy)
    # if key == 'm':
    #     newDemonSpirit = Enemy('demonSpirit', 'Demon Spirit.png', 128,
    #                            random.randrange(0, app.width), random.randrange(0, app.height),
    #                            [2, 2, 200, 1], True)
    #     #print(newDemonSpirit.generateBFSList(wizard.centerX, wizard.centerY, app.width, app.height))
    #     print(newDemonSpirit.enemyAlg2(wizard.centerX, wizard.centerY, app.width, app.height))
    #     app.enemies.append(newDemonSpirit)
    # if key == 't':
    #     app.survival = not app.survival
    #     app.enemies = []
    if key == 'r':
        wizard.status = True
        wizard.centerX = app.width//2
        wizard.centerY = app.height//2
        app.survival = False
        wizard.health = 1000
        wizard.mana = 200
    if key == 'e' and app.survival == False:
        if wizard.checkSpellTableInteraction(app.width, app.height):
            app.PCUpgradeInteract = True
            app.upgrade = True
            app.spellTable = True
        elif wizard.checkWorkshopInteraction(app.width, app.height):
            app.PCUpgradeInteract = True
            app.upgrade = True
            app.workshop = True
        elif wizard.checkCharUpgradeInteraction(app.width, app.height):
            app.PCUpgradeInteract = True
            app.upgrade = True
            app.skillUpgrade = True
    if key == 'escape':
        if app.bookshelf == False:
            app.PCUpgradeInteract = False
            app.upgrade = False
            app.spellTable = False
            app.workshop = False
            app.skillUpgrade = False
        elif app.bookshelf == True:
            app.bookshelf = False
        a, b = app.spellBookSelected
        if a == True:
            app.spellBookSelected = False, -2
    # if key == 'space' and app.canDodge == True:
    #     print('cool')
    #     app.invincibleCounter = 0
    #     app.invincible = True
    #     wizard.dodge(app.img)

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
    # if key == 'space':
    #     app.dodgeCooldown = 0

def perlin(x, y, seed=0):
    x0 = x.astype(int)
    x1 = x0 + 1
    y0 = y.astype(int)
    y1 = y0 + 1

    np.random.seed(seed)
    ptable = np.arange(256, dtype = int)
    np.random.shuffle(ptable)
    ptable = np.stack([ptable, ptable]).flatten()

    distanceX = x - x0
    distanceY = y - y0

    smoothX = fade(distanceX)
    smoothY = fade(distanceY)

    n00 = gradientFunc(ptable[ptable[x0] + y0], x0, y0, x, y)
    n01 = gradientFunc(ptable[ptable[x0] + y0 + 1],x0, y1, x, y)
    n11 = gradientFunc(ptable[ptable[x0 + 1] + y0 + 1], x1, y1, x, y)
    n10 = gradientFunc(ptable[ptable[x0 + 1] + y0],x1, y0, x, y)

    x1LinInterp = lerp(n00, n10, smoothX)
    x2LinInterp = lerp(n01, n11, smoothX)
    return lerp(x1LinInterp, x2LinInterp, smoothY)

def gradientFunc(iteration, integerX, integerY, x, y):
    dx = x - integerX
    dy = y - integerY

    vectors = np.array([[0,1], [0,-1], [1,0], [-1,0]])
    gradient = vectors[iteration % 4]

    return (dx*gradient[:, :, 0] + dy*gradient[:, :, 1])

def lerp(a, b, x):
    return a + x * (b - a)

def fade(z):
    return 6 * z**5 - 15 * z**4 + 10 * z**3

def generateScreenImage(dimX, dimY):
    numArray = np.linspace(1, 3, 10, endpoint = False)
    x, y = np.meshgrid(numArray, numArray)
    seedNum = random.randrange(0, 1000000000)
    # plt.imshow(perlin(x, y, seed=seedNum), origin = 'upper')
    # plt.show()
    imgGrey = Image.fromarray(perlin(x, y, seed = seedNum) * 255, 'I')
    imgGrey = imgGrey.resize((dimX, dimY))
    coordinate = 500, 500
    imgGrey.getpixel(coordinate)
    imgGrey = CMUImage(imgGrey)
    return imgGrey


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
            currImg = screenDict[(self.nodeX, self.nodeY)]
            drawImage(currImg, self.dimX//2, self.dimY//2, align = 'center')
            return
        numArray = np.linspace(1, 3, 10, endpoint = False)
        x, y = np.meshgrid(numArray, numArray)
        seedNum = random.randrange(0, 1000000000)
        img = Image.fromarray(perlin(x, y, seed = seedNum) * 255, 'I')
        img = img.resize((self.dimX, self.dimY))
        coordinate = wizard.centerX, wizard.centerY
        pixel = img.getpixel(coordinate)
        img = CMUImage(img)
        drawImage(img, self.dimX//2, self.dimY//2, align = 'center')
        screenDict[(self.nodeX, self.nodeY)] = img
        return pixel 

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
    
    # def dodge(self, orientation):
    #     print(orientation)
    #     if orientation == 'Player Character V6.png':
    #         self.centerX += 100
    #     elif orientation == 'Player Character V7.png':
    #         self.centerX -= 100
    #     elif orientation == 'PC Up Movement V0.png':
    #         self.centerY -= 100
    #     elif orientation == 'PC Down Movement V0.png':
    #         self.centerY += 100
        
    def checkSpellTableInteraction(self, dimX, dimY):
        if distance(self.centerX, self.centerY, dimX//2 - 150, dimY//2 + 100) <= 64:
            return True
    
    def checkWorkshopInteraction(self, dimX, dimY):
        if distance(self.centerX, self.centerY, dimX//2, dimY//2 - 50) <= 64:
            return True
    
    def checkCharUpgradeInteraction(self, dimX, dimY):
        if distance(self.centerX, self.centerY, dimX//2 + 150, dimY//2 + 100) <= 64:
            return True  

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
    
    def addEnemyUnlock(self):
        app.enemiesUnlocked.append(self)
    
    def interact(self):
        #TODO: make this work for all sprite size enemies (not just 64)
        if distance(self.centerX, self.centerY, wizard.centerX, wizard.centerY) <= 64:
            return True
    
    def displayHealth(self, hfactor):
        drawRect(self.centerX, self.centerY - 64, 74, 20, fill = None, border = 'saddleBrown',
                 borderWidth = 5, align = 'center')
        drawRect(self.centerX + 0, self.centerY - 64, max(2, self.health // hfactor), 10, fill = 'crimson', align = 'center')
    
    def checkStatus(self):
        if self.health <= 2:
            self.status = False

    def enemyAlg1(self, centerX, centerY, wizardCenterX, wizardCenterY):
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

    def generateBFSList(self, wcenterX, wcenterY, dimX, dimY):
        graph = []
        for row in range((dimY // 10)):
            newRow = []
            for col in range((dimX // 10)):
                if distance(self.centerX, self.centerY, col * 10, row * 10) <= 30:
                    newRow.append((row, col))
                    indexRow, indexCol = row, col
                elif distance(wcenterX, wcenterY, col * 10, row * 10) <= 30:
                    newRow.append((row, col))
                    windexRow, windexCol = row, col
                else:
                    newRow.append((row, col))
            graph.append(newRow)
        return (graph, indexRow, indexCol, windexRow, windexCol)
            
    def enemyAlg2(self, wizardCenterX, wizardCenterY, dimX, dimY):
        moves = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
        res = self.generateBFSList(wizardCenterX, wizardCenterY, dimX, dimY)
        nodeGraph = res[0]
        startRow, startCol, targetRow, targetCol = res[1], res[2], res[3], res[4]
        startQueue = [(startRow, startCol)]
        visitedNodes = set()
        visitedNodes.add((startRow, startCol))
        nodeDict = dict()      
        while startQueue != []:
            currentNode = startQueue.pop(0)
            if currentNode == (targetRow, targetCol):
                path = [currentNode]
                pathNode = currentNode
                while pathNode != (startRow, startCol):
                    nextNode = nodeDict[pathNode]
                    path.append(nextNode)
                    pathNode = nextNode
                return path
            else:
                for move in moves:
                    if (currentNode[0] + move[0] < 0 or currentNode[0] + move[0] >= len(nodeGraph) or
                        currentNode[1] + move[1] < 0 or currentNode[1] + move[1] >= len(nodeGraph[0])):
                            continue
                    n = nodeGraph[currentNode[0] + move[0]][currentNode[1] + move[1]]
                    if n not in visitedNodes:
                        visitedNodes.add(n)
                        startQueue.append(n)
                        nodeDict[(currentNode[0] + move[0], currentNode[1]+ move[1])] = (currentNode[0], currentNode[1])
        return None
                    
def scrambleWords(wordList, result):
    if wordList == []:
        return result
    else:
        currWord = wordList[0]
        remaining = wordList[1:]
        if len(currWord) > 1:
            currWordList = []
            for c in currWord:
                currWordList.append(c)
            scrambledWord = ''
            while len(currWordList) > 0:
                r = random.choice(currWordList)
                scrambledWord += r
                currWordList.remove(r)
            if scrambledWord == currWord:
                return scrambleWords(wordList, result)
            if len(wordList) == 1:
                result += scrambledWord
            else:
                result += scrambledWord + ' '
        elif len(wordList) == 1:
            result += currWord
        else:
            result += currWord + ' '
        return scrambleWords(remaining, result)

class SpellBook:
    def __init__(self, text, spellUnlock, reqMaterials, status, unscrambledStatus):
        self.text = text
        self.spellUnlock = spellUnlock
        self.reqMaterials = reqMaterials
        self.status = status
        self.unscrambledStatus = unscrambledStatus
        self.scrambledText = None
    
    def activateSpellBook(self):
        self.status = True
        plainTextList = self.text.split(' ')
        scrambledText = scrambleWords(plainTextList, '')
        return scrambledText
    
    def checkSolveStatus(self, solveAttempt):
        print(repr(solveAttempt), repr(self.text))
        if solveAttempt == self.text:
            self.unscrambledStatus = False
        else:
            self.unscrambledStatus = True
        return self.unscrambledStatus

wizard = Character(app.width//2, app.height//2)

def main():
    runApp()

main()