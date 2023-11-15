from cmu_graphics import *

def onAppStart(app):
    app.titleScreen = True
    app.titleURL = 'https://cdn.discordapp.com/attachments/1089215878601654355/1173748555442307072/image.png?ex=65651586&is=6552a086&hm=e1ab7dbfd8acddc40a13f9d2eccd096a49e4cf8b669f8827a6257f19583c9262&'
    # app.startGameURL = 'https://cdn.discordapp.com/attachments/1089215878601654355/1173752340042481674/generatedtext_3.jpg?ex=6565190d&is=6552a40d&hm=c8c17359e16c4a4bd3e208a382947833231e49a0bfa5a39c14971e16510514dc&'
    # app.loadGameURL = 'https://media.discordapp.net/attachments/1089215878601654355/1173754082092126248/generatedtext_3.jpg?ex=65651aac&is=6552a5ac&hm=88e317186b74aed4e457dda1f6e34a0411c561f0fbf388ce34cd4c81fce63b4f&=&width=265&height=72'
    # app.settingsURL = 'https://cdn.discordapp.com/attachments/1089215878601654355/1173756686746538005/load_game_image.jpg?ex=65651d19&is=6552a819&hm=08c6b1a46605f9bc1125e7755c07049d1dd26efc62ff29d3064708d1d93d1894&'
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
    
    app.firstPrompt = True
    app.secondPrompt = False
    app.thirdPrompt = False

    app.stepsPerSecond = 50

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
        drawImage(app.titleURL, app.width//2, app.height//4, align = 'center',
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

def main():
    runApp()

main()