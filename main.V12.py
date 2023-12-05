from cmu_graphics import *
from PIL import Image
import random
import numpy as np
import os, pathlib
import statistics
import ctypes

def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

def onAppStart(app):
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    app.width = screensize[0]
    app.height = screensize[1]

    app.titleScreen = True

    app.survivalMusic = loadSound('ChopinBMinorSonata.mp3')

    app.downTimeMusic = loadSound('ChopinPrelude6.mp3')

    app.fireball = loadSound('Fireball Cast.mp3')
    app.lightningSerpent = loadSound('Lightning Serpent Sound Effect.mp3')

    app.titleScreenMusic = loadSound('Slavonic_Dances_TP.mp3')
    app.titleScreenMusic.play(loop = True)

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
    app.prevNodeX = None
    app.prevNodeY = None
    app.img = 'Player Character V6.png'

    app.enemies = []

    app.spells = []

    app.inventory = dict()
    app.inventory[None] = 1
    app.PCSpellsUnlocked = []
    app.spellSelected = []
    app.spellDisplayImg = None
    app.spellBook = None
    app.drawSpellbook = False

    
    app.manaRegenRate = 10
    app.count = 0

    app.enemiesUnlocked = []

    app.upgrade = False
    app.PCUpgradeInteract = False
    app.spellTable = False
    app.spellBooksCollected = [SpellBook("A Basic Spell Only Requiring A Little Ingenuity.", 
                                         'fireball', [(None, 0)], False, False, 
                                         Projectile('fireballI', 'Fireball I.png', 50, 
                                        wizard.centerX, wizard.centerY, [20], True,
                                        app.fireball))]
    app.spellBookSelected = False, -2
    app.bookshelf = False
    app.displayDecryptResTrue = False
    app.displayDecryptResFalse = False
    app.learnSpell = False
    app.lackMaterials = False
    app.lackNumMaterials = False

    app.workshopInteract = False
    app.skillUpgrade = False

    app.survival = False

    app.invincible = False
    app.invincibleCounter = 0
    app.dodgeCooldown = 0
    app.canDodge = True

    #app.downtime = DowntimeCountdown()
    # app.downtime.start()

    app.totalCounter = 20 * 20
    app.roundNum = 1
    app.timerColor = 'blue'

    app.roundMax = 4
    app.win = False

    app.items = []
    app.spellBooks = []
    app.drawItem = False
    app.item = None

    app.key = 0
    app.healthflasks = 3

    app.MainScreen = Image.open('Main Screen Background.png')
    app.MainScreen = app.MainScreen.resize((app.width, app.height))
    app.MainScreen = CMUImage(app.MainScreen)

    app.fortress = CMUImage(Image.open('Blackstone Fortress.png'))
    app.spellbook = CMUImage(Image.open('Spellbook Table.png'))
    app.workshop = CMUImage(Image.open('Workshop.png'))
    app.portal = CMUImage(Image.open('Portal.png'))

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
    
    elif app.moveRight == True:
        currScreen = smallScreen(app.width, app.height, app.nodeX, app.nodeY)
        currpixel = currScreen.drawScreen(app.MainScreen, app.fortress, app.spellbook, app.workshop, app.portal)
        if currpixel != None and currpixel > 0 and not (app.nodeX == 0 and app.nodeY == 0):
            wizard.takeDamage(50)
        if app.drawItem == True:
            drawImage(CMUImage(Image.open(app.item[0])), app.item[1], app.item[2], align = 'center')
        if app.drawSpellbook == True:
            drawImage(CMUImage(Image.open('Spellbook Item.png')),
                      app.spellBook[0], app.spellBook[1], align = 'center')
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
        currpixel = currScreen.drawScreen(app.MainScreen, app.fortress, app.spellbook, app.workshop, app.portal)
        if currpixel != None and currpixel > 0 and not (app.nodeX == 0 and app.nodeY == 0):
            wizard.takeDamage(50)
        if app.drawItem == True:
            drawImage(CMUImage(Image.open(app.item[0])), app.item[1], app.item[2], align = 'center')
        if app.drawSpellbook == True:
            drawImage(CMUImage(Image.open('Spellbook Item.png')),
                      app.spellBook[0], app.spellBook[1], align = 'center')
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
        currpixel = currScreen.drawScreen(app.MainScreen, app.fortress, app.spellbook, app.workshop, app.portal)
        if currpixel != None and currpixel > 0 and not (app.nodeX == 0 and app.nodeY == 0):
            wizard.takeDamage(50)
        if app.drawItem == True:
            drawImage(CMUImage(Image.open(app.item[0])), app.item[1], app.item[2], align = 'center')
        if app.drawSpellbook == True:
            drawImage(CMUImage(Image.open('Spellbook Item.png')),
                      app.spellBook[0], app.spellBook[1], align = 'center')
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
        currpixel = currScreen.drawScreen(app.MainScreen, app.fortress, app.spellbook, app.workshop, app.portal)
        if currpixel != None and currpixel > 0 and not (app.nodeX == 0 and app.nodeY == 0):
            wizard.takeDamage(50)
        if app.drawItem == True:
            drawImage(CMUImage(Image.open(app.item[0])), app.item[1], app.item[2], align = 'center')
        if app.drawSpellbook == True:
            drawImage(CMUImage(Image.open('Spellbook Item.png')),
                      app.spellBook[0], app.spellBook[1], align = 'center')
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
        currpixel = currScreen.drawScreen(app.MainScreen, app.fortress, app.spellbook, app.workshop, app.portal)
        if currpixel != None and currpixel > 0 and not (app.nodeX == 0 and app.nodeY == 0):
            wizard.takeDamage(50)
        if app.drawItem == True:
            drawImage(CMUImage(Image.open(app.item[0])), app.item[1], app.item[2], align = 'center')
        if app.drawSpellbook == True:
            drawImage(CMUImage(Image.open('Spellbook Item.png')),
                      app.spellBook[0], app.spellBook[1], align = 'center')
        wizard.drawHealthandMana()
        wizard.drawChar(app.img)
        drawLabel(f'{app.totalCounter//(20 * 60)}m, {(app.totalCounter // 20) % 60}s',
                  app.width - 20, 20, align = 'right-top', 
                  font = 'monospace', size = 30, fill = app.timerColor)
    #checkSpellTableInteraction  checkWorkshopInteraction checkCharUpgradeInteraction
    if app.survival == False:
        if app.thirdPrompt == None and app.introCinematic == False:
            drawLabel(f'{app.healthflasks} healing potions', app.width - 20, 50, align = 'right-top',
                  font = 'monospace', size = 20, fill = 'orange')
        if wizard.checkSpellTableInteraction(app.width, app.height) and app.PCUpgradeInteract == True:
            drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 80)
            drawImage(CMUImage(Image.open('Upgrade Canvas.png')), 
                    app.width//2, app.height//2, align = 'center')
            
            a, b = app.spellBookSelected
            if a == True and len(app.spellBooksCollected) > b:
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
    if app.spellDisplayImg != None:
        drawLabel(app.spellSelected.projectile.name, 93, app.height - 20, align = 'center',
                  font = 'monospace', size = 20, fill = 'yellow')
        if type(app.spellDisplayImg) == list:
            drawImage(CMUImage(Image.open(app.spellDisplayImg[0])), 93, app.height - 60, align = 'center')
        else:
            drawImage(CMUImage(Image.open(app.spellDisplayImg)), 93, app.height - 60, align = 'center')
    
    for spell in app.spells:
        if spell[0].status == True:
            spell[0].drawProjectile(app.width, app.height, spell[0].stats[-1])
    
    if app.survival == True:
        drawLabel(f'{app.healthflasks} healing potions', app.width - 20, 50, align = 'right-top',
                  font = 'monospace', size = 20, fill = 'orange')
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
                    enemy.checkProjectile(spell[0], spell[1], spell[2], spell[3])
                    enemy.checkStatus()
        
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 30)
    
    if wizard.status == False:
        drawRect(0, 0, app.width, app.height, fill = 'black',)
        drawLabel('YOU DIED', app.width//2, app.height//2, fill = 'red', font = 'monospace')
    
    elif app.win == True:
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
        app.titleScreen = False
        app.firstPrompt  = True
        app.introCinematic = False
        app.thirdPrompt = None
    # if app.introCinematic == True:
    #     app.introCinematic = False
    #     app.thirdPrompt = None
    #     #app.win = True
        #endGame()
    if app.introCinematic == False and app.thirdPrompt == None and app.items == []:
        app.items = [Item(800, 'Lightning Essence', 'Lightning Essence.png', app.width, app.height)]

        app.spellBooks = [SpellBook("Harness The Power Of Thunder With 5 Essence.", 
                                         'Lightning Serpent', [('Lightning Essence', 1)], False, False, 
                                         Projectile('Lightning Serpent', 
                                                    ['Lightning Bolt1.png', 'Lightning Bolt2.png',
                                                     'Lightning Bolt3.png', 'Lightning Bolt4.png',], 
                                                    250, 
                                                    wizard.centerX, wizard.centerY, [50], True,
                                                    'Lightning Serpent Sound Effect.mp3'))]



    elif (app.introCinematic == False and app.thirdPrompt == None and app.upgrade == False
          and app.spellSelected != None and len(app.PCSpellsUnlocked) > 0):
        if app.PCSpellsUnlocked[int(app.key) - 1].projectile.name == 'fireballI':
            newSpell = Projectile('fireballI', 'Fireball I.png', 50, 
                                        wizard.centerX, wizard.centerY, [20], True,
                                        app.fireball)
    
        elif app.spellSelected.projectile.name=='Lightning Serpent':
            newSpell = Projectile('Lightning Serpent', 
                                                    ['Lightning Bolt1.png', 'Lightning Bolt2.png',
                                                     'Lightning Bolt3.png', 'Lightning Bolt4.png',], 
                                                    250, 
                                                    wizard.centerX, wizard.centerY, [120], True,
                                                    app.lightningSerpent)
        newSpell.stats.append(app.img)
        newSpell.playProjectileSound(newSpell.audioFile)
        app.spells.append((newSpell, app.img, wizard.centerX, wizard.centerY))
        if wizard.mana < newSpell.stats[0]:
            newSpell.status = False
        if newSpell.status == True and wizard.mana - newSpell.stats[0] <= 0:
            wizard.mana = 2
        elif newSpell.status == True:
            wizard.mana -= newSpell.stats[0]
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
                            app.PCSpellsUnlocked.append(app.spellBooksCollected[app.spellBookSelected[1]])
                            app.learnSpell = True
                            app.spellBooksCollected.pop(app.spellBookSelected[1])
                        elif app.inventory[currMaterial] == numMaterial:
                            del app.inventory[currMaterial]
                            app.PCSpellsUnlocked.append(app.spellBooksCollected[app.spellBookSelected[1]])
                            app.learnSpell = True
                            app.spellBooksCollected.pop(app.spellBookSelected[1])
                        else:
                            app.lackNumMaterials = True
                    else:
                        app.lackMaterials = True
# def endGame():
#     app.paused = True
                
def onStep(app):
    if app.win == True:
        app.survival == False
        return
    if app.titleScreen == False:
        app.titleScreenMusic.pause()
        if app.totalCounter == 20 * 20 and app.roundNum == 1 and app.survival == False:
            app.downTimeMusic.play(loop = True, restart = True)
    if app.thirdPrompt == None and app.introCinematic == False:
        app.totalCounter -= 1
    for enemy in app.enemies:
        if enemy.name == 'demonSpirit':
            enemy.stats[3] += 1
    #TODO: make item spawn one attempt to utilize random chance
    if (app.thirdPrompt == None and app.introCinematic == False and app.drawItem == False
        and (app.nodeX != 0 or app.nodeY != 0) 
        and (app.nodeX != app.prevNodeX or app.nodeY != app.prevNodeY)):
            currItemIndex = random.randrange(0, len(app.items))
            app.item = app.items[currItemIndex].getLocation()
            if app.item != None:
                app.drawItem = True
                app.prevNodeX = app.nodeX
                app.prevNodeY = app.nodeY
    if (app.thirdPrompt == None and app.introCinematic == False and app.drawSpellbook == False
        and app.nodeX == 0 and app.nodeY == 0 and app.roundNum == 2 and app.survival == False):
            currSpellBookIndex = random.randrange(0, len(app.spellBooks))
            app.spellBook = app.spellBooks[currSpellBookIndex].getSpellBookLocation(app.width, app.height)
            if app.spellBook != None:
                app.drawSpellbook = True
            if app.spellBooksCollected != [] and app.spellBook[2] in app.spellBooksCollected:
                app.drawSpellbook = False
    if app.survival == True:
        app.nodeX = 0
        app.nodeY = 0
    if app.totalCounter <= 0:
        if app.survival == True:
            app.enemies = []
            app.spells = []
            app.survival = False
            app.timerColor = 'blue'
            app.roundNum += 1
            app.prevNodeX == None
            app.prevNodeY == None
            app.downTimeMusic.play(loop = True, restart = True)
            app.survivalMusic.pause()
            if app.roundNum >= app.roundMax:
                app.win = True
                #endGame()
            app.totalCounter = (90 * 20) #* app.roundNum
        elif app.survival == False:
            app.survival = True
            app.survivalMusic.play(loop = True, restart = True)
            app.downTimeMusic.pause()
            app.timerColor = 'red'
            app.totalCounter = (20 * 20)
    if app.survival == True:
        ranNum = random.randrange(0, 1000)
        if ranNum >= 995 and app.roundNum >= 3:
            newEnemy =  Enemy('demonSpirit', 'Demon Spirit.png', 128,
                                random.randrange(0, app.width), random.randrange(0, app.height),
                                [2, 2, 200, 1], True)
            app.enemies.append(newEnemy)
        elif ranNum >= 985 and app.roundNum >= 2:
            newEnemy = Enemy('evilDummy', 'Evil Dummy.png', 256,
                                random.randrange(0,app.width), random.randrange(0,app.height),
                                [1, 4, 100], True)
            app.enemies.append(newEnemy)
        elif ranNum >= 990 and app.roundNum >= 1:
            newEnemy =  Enemy('testDummy', 'Test Dummy.png', 64, 
                                random.randrange(0,app.width), random.randrange(0,app.height), 
                                [0, 1, 0], True)
            app.enemies.append(newEnemy)
    app.invincibleCounter += 1
    if app.invincibleCounter % 40 == 0:
            app.invincibleCounter = False
    app.dodgeCooldown = min(app.dodgeCooldown + 1, 20)
    if app.dodgeCooldown % 20 == 0:
        app.canDodge = True
    else:
        app.canDodge = False
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
    if app.thirdPrompt == None:
        app.introCinematic = False
    if app.moveRight == True:
        if wizard.centerX >= app.width:
            app.nodeX += 1
            app.drawItem = False
            wizard.centerX = 10
    if app.moveLeft == True:
        if wizard.centerX <= 0: 
            app.nodeX -= 1
            app.drawItem = False
            wizard.centerX = app.width - 10
    if app.moveUp == True:
        if wizard.centerY <= 0:
            app.nodeY += 1
            app.drawItem = False
            wizard.centerY = app.height - 10
    if app.moveDown == True:
        if wizard.centerY >= app.height:
            app.nodeY -= 1
            app.drawItem = False
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
        elif app.spells[j][0].status == False:
            app.spells.pop(j)
    if app.moveRight == True:
        app.img = f'Player Character Right Movement V{wizard.rightCount}.png'
    elif app.moveLeft == True:
        app.img = f'Player Character Left Movement V{wizard.leftCount}.png'
    elif app.moveUp == True:
        app.img = f'PC Up Movement V{wizard.upCount}.png'
    elif app.moveDown == True:
        app.img = f'PC Down Movement V{wizard.leftCount}.png'
    
    

def onKeyPress(app, key):
    if app.upgrade == False:
        if key == 'd': 
            app.moveRight = True
        if key == 'a':
            app.moveLeft = True
        if key == 'w':
            app.moveUp = True
        if key == 's':
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
    #     
    #     app.enemies.append(newDemonSpirit)
    # if key == 't':
    #     app.survival = not app.survival
    #     app.enemies = []
    if key == 'r' and wizard.status == False:
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
            app.workshopInteract = True
        elif wizard.checkCharUpgradeInteraction(app.width, app.height):
            app.PCUpgradeInteract = True
            app.upgrade = True
            app.skillUpgrade = True
    if key in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and int(key) <= len(app.PCSpellsUnlocked):
        app.spellSelected = app.PCSpellsUnlocked[int(key) - 1]
        app.key = key
        app.spellDisplayImg = app.PCSpellsUnlocked[int(key) - 1].projectile.img
    if key == 'escape':
        if app.bookshelf == False:
            app.PCUpgradeInteract = False
            app.upgrade = False
            app.spellTable = False
            app.workshopInteract = False
            app.skillUpgrade = False
            app.learnSpell = False
            app.displayDecryptResTrue = False
            app.displayDecryptResFalse = False
        elif app.bookshelf == True:
            app.bookshelf = False
        a, b = app.spellBookSelected
        if a == True:
            app.spellBookSelected = False, -2
    if key == 'f' and app.item != None and wizard.pickUpItem(app.item[1], app.item[2]):
        if app.item[3] in app.inventory:
            app.inventory[app.item[3]] += 1
        else:
            app.inventory[app.item[3]] = 1
        app.drawItem = False
    if key == 'f' and app.spellBook != None and wizard.getSpellBook(app.spellBook[0], app.spellBook[1]):
        app.spellBooksCollected.append(app.spellBook[2])
        app.drawSpellbook = False
    if key == 'h':
        if app.healthflasks > 0:
            wizard.health = min(wizard.health + 600, 1000)
            app.healthflasks -= 1
        else:
            app.healthflasks = 0
        
    if key == 'space' and app.canDodge == True:
        wizard.dodge(app.img)
        if wizard.centerX >= app.width:
            app.nodeX += 1
            app.drawItem = False
            wizard.centerX = 10
        if wizard.centerX <= 0:
            app.nodeX -= 1
            app.drawItem = False
            wizard.centerX = app.width - 10
        if wizard.centerY >= app.height:
            app.nodeY -= 1
            app.drawItem = False
            wizard.centerY = 10
        if wizard.centerY <= 0:
            app.nodeY += 1
            app.drawItem = False
            wizard.centerY = app.height - 10

def onKeyRelease(app, key):
    if key == 'd':
        app.img = 'Player Character V6.png'
        app.moveRight = False
    if key == 'a':
        app.img = 'Player Character V7.png'
        app.moveLeft = False
    if key == 'w':
        app.img = 'PC Up Movement V0.png'
        app.moveUp = False
    if key == 's':
        app.img = 'PC Down Movement V0.png'
        app.moveDown = False
    if key == 'space':
        if key == 'space' and app.canDodge == True:
            app.dodgeCooldown = 0
            app.invincible = True

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

# def generateScreenImage(dimX, dimY):
#     numArray = np.linspace(1, 3, 10, endpoint = False)
#     x, y = np.meshgrid(numArray, numArray)
#     seedNum = random.randrange(0, 1000000000)
#     # plt.imshow(perlin(x, y, seed=seedNum), origin = 'upper')
#     # plt.show()
#     imgGrey = Image.fromarray(perlin(x, y, seed = seedNum) * 255, 'I')
#     imgGrey = imgGrey.resize((dimX, dimY))
#     coordinate = 500, 500
#     imgGrey.getpixel(coordinate)
#     imgGrey = CMUImage(imgGrey)
#     return imgGrey


class smallScreen:
    def __init__(self, dimX, dimY, nodeX, nodeY):
        self.dimX = dimX
        self.dimY = dimY
        self.nodeX = nodeX
        self.nodeY = nodeY

    def drawScreen(self, mainScreen, fortress, spellbook, workshop, portal):
        if self.nodeX == 0 and self.nodeY == 0:
            drawImage(mainScreen, self.dimX//2, self.dimY//2, align = 'center')
            drawImage(fortress, self.dimX//2, self.dimY//2, align = 'center')
            drawImage(spellbook, self.dimX//2 - 150, self.dimY//2 + 100, align = 'center')
            drawImage(workshop, self.dimX//2, self.dimY//2 - 50, align = 'center')
            drawImage(portal, self.dimX//2, self.dimY//2 + 100, align = 'center')
            # drawImage(CMUImage(Image.open('Blackstone Fortress.png')), 
            #           self.dimX//2, self.dimY//2, align = 'center')
            # drawImage(CMUImage(Image.open('Spellbook Table.png')), 
            #           self.dimX//2 - 150, self.dimY//2 + 100, align = 'center')
            # drawImage(CMUImage(Image.open('Workshop.png')),
            #           self.dimX//2, self.dimY//2 - 50, align = 'center')
            # drawImage(CMUImage(Image.open('Portal.png')),
            #           self.dimX//2, self.dimY//2 + 100, align = 'center')
            drawCircle(self.dimX//2 + 150, self.dimY//2 + 100, 32, fill = None, border = 'white',
                       borderWidth = 10)
            drawStar(self.dimX//2 + 150, self.dimY//2 + 100, 32, 4, fill = None, border = 'white',
                     borderWidth = 5)
            return
        elif (self.nodeX, self.nodeY) in screenDict:
            currImg = screenDict[(self.nodeX, self.nodeY)]
            coordinate = (statistics.median([0, wizard.centerX, self.dimX]), statistics.median([0, wizard.centerY, self.dimY]))
            currImg = currImg.resize((self.dimX, self.dimY))
            pixel = currImg.getpixel(coordinate)
            drawImage(CMUImage(currImg), self.dimX//2, self.dimY//2, align = 'center')
            return pixel
        numArray = np.linspace(1, 3, 10, endpoint = False)
        x, y = np.meshgrid(numArray, numArray)
        seedNum = random.randrange(0, 1000000000)
        img = Image.fromarray(perlin(x, y, seed = seedNum) * 255, 'I')
        img = img.resize((self.dimX, self.dimY))
        coordinate = wizard.centerX, wizard.centerY
        pixel = img.getpixel(coordinate)
        screenDict[(self.nodeX, self.nodeY)] = img
        img = CMUImage(img)
        drawImage(img, self.dimX//2, self.dimY//2, align = 'center')
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

        self.img = None

        self.status = True

        self.InvTimer = 1
    
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
        self.InvTimer -= 1
        if self.InvTimer == 0:
            if self.health - damage <= 2:
                self.health = 2
                self.InvTimer = 0.5 * 20
                self.status = False
            else:
                self.health -= damage
                self.InvTimer = 0.5 * 20
    
    def dodge(self, orientation):
        if orientation in {'Player Character V6.png', 'Player Character Right Movement V0.png',
                               'Player Character Right Movement V1.png',
                               'Player Character Right Movement V2.png',
                               'Player Character Right Movement V3.png',}:
            self.centerX += 150
        elif orientation in {'Player Character V7.png', 'Player Character Left Movement V0.png',
                               'Player Character Left Movement V1.png',
                               'Player Character Left Movement V2.png',
                               'Player Character Left Movement V3.png',}:
            self.centerX -= 150
        elif orientation in {'PC Up Movement V0.png', 'PC Up Movement V1.png',
                                 'PC Up Movement V2.png', 'PC Up Movement V3.png',}:
            self.centerY -= 150
        elif orientation in {'PC Down Movement V0.png', 'PC Down Movement V1.png',
                                 'PC Down Movement V2.png', 'PC Down Movement V3.png',}:
            self.centerY += 150
        
    def checkSpellTableInteraction(self, dimX, dimY):
        if distance(self.centerX, self.centerY, dimX//2 - 150, dimY//2 + 100) <= 64:
            return True
    
    def checkWorkshopInteraction(self, dimX, dimY):
        if distance(self.centerX, self.centerY, dimX//2, dimY//2 - 50) <= 64:
            return True
    
    def checkCharUpgradeInteraction(self, dimX, dimY):
        if distance(self.centerX, self.centerY, dimX//2 + 150, dimY//2 + 100) <= 64:
            return True  
    
    def pickUpItem(self, itemXcord, itemYcord):
        if distance(self.centerX, self.centerY, itemXcord, itemYcord) <= 100:
            return True
    
    def getSpellBook(self, x, y):
        if distance(self.centerX, self.centerY, x, y) <= 100:
            return True

class Projectile:
    def __init__(self, name, img, rawDamage, startX, startY, stats, status, audioFile):
        self.name = name
        self.img = img
        self.rawDamage = rawDamage
        self.centerX = startX
        self.centerY = startY
        self.stats = stats
        self.status = status
        self.counter = 0
        self.lightningSpellTimer = 2 * 20
        self.audioFile = audioFile
    
    def drawProjectile(self, dimX, dimY, orientation):
        if type(self.img) != list:
            drawImage(CMUImage(Image.open(f'{self.img}')), 
                        self.centerX, self.centerY, align = 'center')
            if orientation in {'Player Character V6.png', 'Player Character Right Movement V0.png',
                               'Player Character Right Movement V1.png',
                               'Player Character Right Movement V2.png',
                               'Player Character Right Movement V3.png', 
                               'Player Character Right Movement V6.png'}:
                self.centerX += 30
            elif orientation in {'Player Character V7.png', 'Player Character Left Movement V0.png',
                               'Player Character Left Movement V1.png',
                               'Player Character Left Movement V2.png',
                               'Player Character Left Movement V3.png',}:
                self.centerX -= 30
            elif orientation in {'PC Up Movement V0.png', 'PC Up Movement V1.png',
                                 'PC Up Movement V2.png', 'PC Up Movement V3.png',}:
                self.centerY -= 30
            elif orientation in {'PC Down Movement V0.png', 'PC Down Movement V1.png',
                                 'PC Down Movement V2.png', 'PC Down Movement V3.png',}:
                self.centerY += 30
            if (self.centerX < 0 or self.centerX > dimX or
                self.centerY < 0 or self.centerY > dimY):
                    self.status = False
        else:
            if orientation in {'Player Character V6.png', 'Player Character Right Movement V0.png',
                               'Player Character Right Movement V1.png',
                               'Player Character Right Movement V2.png',
                               'Player Character Right Movement V3.png',}:
                drawImage(CMUImage(Image.open(self.img[self.counter % len(self.img)])),
                      self.centerX, self.centerY, align = 'left-bottom', rotateAngle = 0)
            elif orientation in {'Player Character V7.png', 'Player Character Left Movement V0.png',
                               'Player Character Left Movement V1.png',
                               'Player Character Left Movement V2.png',
                               'Player Character Left Movement V3.png',}:
                drawImage(CMUImage(Image.open(self.img[self.counter % len(self.img)])),
                      self.centerX, self.centerY, align = 'right-bottom', rotateAngle = 180)
            elif orientation in {'PC Up Movement V0.png', 'PC Up Movement V1.png',
                                 'PC Up Movement V2.png', 'PC Up Movement V3.png',}:
                drawImage(CMUImage(Image.open(self.img[self.counter % len(self.img)])),
                      self.centerX, self.centerY, align = 'right-bottom', rotateAngle = 90)
            elif orientation in {'PC Down Movement V0.png', 'PC Down Movement V1.png',
                                 'PC Down Movement V2.png', 'PC Down Movement V3.png',}:
                drawImage(CMUImage(Image.open(self.img[self.counter % len(self.img)])),
                        self.centerX, self.centerY, align = 'right-top', rotateAngle = 270)
            self.counter += 1
            self.lightningSpellTimer -= 1
            if self.lightningSpellTimer <= 0:
                self.status = False
        
    def playProjectileSound(self, audio):
        audio.play(restart = True)



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
    
    def checkProjectile(self, projectile, orientation, x, y):
        if type(projectile.img) == list:
            img = Image.open(projectile.img[0])
            if orientation in {'Player Character V6.png', 'Player Character Right Movement V0.png',
                               'Player Character Right Movement V1.png',
                               'Player Character Right Movement V2.png',
                               'Player Character Right Movement V3.png',}:
                if (x <= self.centerX <= x + img.width and
                    y - (img.height // 2) <= self.centerY <= y + (img.height // 2)):
                        self.takeDamage(projectile)
            elif orientation in {'Player Character V7.png', 'Player Character Left Movement V0.png',
                               'Player Character Left Movement V1.png',
                               'Player Character Left Movement V2.png',
                               'Player Character Left Movement V3.png',}:
                if (x - img.width <= self.centerX <= x + img.width and
                    y - (img.height // 2) <= self.centerY <= y + (img.height // 2)):
                        self.takeDamage(projectile)
            elif orientation in {'PC Up Movement V0.png', 'PC Up Movement V1.png',
                                 'PC Up Movement V2.png', 'PC Up Movement V3.png',}:
                if (x - img.height // 2 <= self.centerX <= x + img.height // 2 and
                    y - img.width <= self.centerY <= y):
                        self.takeDamage(projectile)
            elif orientation in {'PC Down Movement V0.png', 'PC Down Movement V1.png',
                                 'PC Down Movement V2.png', 'PC Down Movement V3.png',}:
                if (x - img.height // 2 <= self.centerX <= x + img.height // 2 and
                    y <= self.centerY <= y + img.width):
                        self.takeDamage(projectile)
        else:
            if distance(self.centerX, self.centerY, projectile.centerX, projectile.centerY) <= Image.open(projectile.img).width:
                self.takeDamage(projectile)
                projectile.status = False

    def takeDamage(self, projectile):
        self.health = max(2, self.health - projectile.rawDamage)
    
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
            return True
        if centerX < wizardCenterX and centerY < wizardCenterY:
            centerX += int(((8 ** 2) * 0.5) ** 0.5)
            centerY += int(((8 ** 2) * 0.5) ** 0.5)
        if centerX < wizardCenterX and centerY > wizardCenterY:
            centerX += int(((8 ** 2) * 0.5) ** 0.5)
            centerY -= int(((8 ** 2) * 0.5) ** 0.5)
        if centerX > wizardCenterX and centerY > wizardCenterY:
            centerX -= int(((8 ** 2) * 0.5) ** 0.5)
            centerY -= int(((8 ** 2) * 0.5) ** 0.5)
        if centerX > wizardCenterX and centerY < wizardCenterY:
            centerX -= int(((8 ** 2) * 0.5) ** 0.5)
            centerY += int(((8 ** 2) * 0.5) ** 0.5)
        if centerX < wizardCenterX and centerY == wizardCenterY:
            centerX += 8
        if centerX > wizardCenterX and centerY == wizardCenterY:
            centerX -= 8
        if centerX == wizardCenterX and centerY < wizardCenterY:
            centerY += 8
        if centerX == wizardCenterX and centerY > wizardCenterY:
            centerY -= 8
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
    def __init__(self, text, spellUnlock, reqMaterials, status, unscrambledStatus, projectile):
        self.text = text
        self.spellUnlock = spellUnlock
        self.reqMaterials = reqMaterials
        self.status = status
        self.unscrambledStatus = unscrambledStatus
        self.scrambledText = None
        self.projectile = projectile
    
    def activateSpellBook(self):
        self.status = True
        plainTextList = self.text.split(' ')
        scrambledText = scrambleWords(plainTextList, '')
        return scrambledText
    
    def checkSolveStatus(self, solveAttempt):
        if solveAttempt == self.text:
            self.unscrambledStatus = False
        else:
            self.unscrambledStatus = True
        return self.unscrambledStatus
    
    def getSpellBookLocation(self, dimX, dimY):
        #TODO: Implement random chance of spawn
        rNum = random.randrange(0, 1000)
        rNumX = random.randrange(0, dimX)
        rNumY = random.randrange(0, dimY)
        return rNumX, rNumY, self

class Item:
    def __init__(self, probabilityNum, name, img, dimX, dimY):
        self.pNum = probabilityNum
        self.img = img
        self.dimX = dimX
        self.dimY = dimY
        self.name = name

    def getLocation(self):
        rNum = random.randrange(0, 1000)
        rNumX = random.randrange(0, self.dimX)
        rNumY = random.randrange(0, self.dimY)
        if rNum >= self.pNum:
            return self.img, rNumX, rNumY, self.name
        return None


wizard = Character(app.width//2, app.height//2)

def main():
    runApp()

main()