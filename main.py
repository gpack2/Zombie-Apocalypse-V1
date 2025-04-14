from player import Player
from zombie import Zombie
from bullet import Bullet
from cmu_graphics import *

def onAppStart(app):
    app.startScreen = True
    restartGame(app)

def restartGame(app):
    app.width = 750
    app.height = 750

    app.roadWidth = app.width/5
    app.buildingWidth = app.buildingHeight = 2 * app.roadWidth

    app.player = Player(app)

    app.currentWave = 0
    app.zombies = getZombiesList(app)
    app.inRound = False
    
    app.startMessageX = app.width/2
    app.startMessageY = 50
    app.startMessageWidth = 300
    app.startMessageHeight = 50

    app.skipMessageWidth = app.startMessageWidth + 110

    app.timer = 120
    app.numSteps = 0

    app.bullets = []
    app.bulletSpeed = 5

    app.gunMenuOpen = False
    app.armoryMenuOpen = False
    app.gunUpgradeCost = 50
    app.gunUpgrade = 5
    app.shieldUpgradeCost = 25
    app.shieldUpgrade = 100

    app.buyMenuBackgroundX = app.width/2
    app.buyMenuBackgroundY = app.height/2 + 50
    app.buyMenuBackgroundHeight = app.height*3/4

    app.buyBoxX = app.buyMenuBackgroundX
    app.buyBoxY = (app.buyMenuBackgroundY) + (app.buyMenuBackgroundHeight)/4
    app.buyBoxWidth = 200
    app.buyBoxHeight = 50
    app.startScreen = True 

    app.playerWon = False

def redrawAll(app):
    if app.startScreen:
        drawStartScreen(app)
    else:
        drawBackground(app)

    
    if app.inRound:
        # draw zombies
        for zombie in app.zombies:
            drawZombie(app, zombie)
        # draw bullets
        for bullet in app.bullets:
            drawCircle(bullet.bx, bullet.by, bullet.radius, fill='black')

    # draw player
    if app.player.isAlive and not app.startScreen:
        drawPlayer(app, app.player)
        
    # draw UI
    if not app.startScreen and not app.playerWon:
        drawUI(app)

    # draw buy menus
    if app.gunMenuOpen:
        drawGunMenu(app)
    elif app.armoryMenuOpen:
        drawArmoryMenu(app)
    
    if app.player.isAlive:
        for bullet in app.bullets:
            drawCircle(bullet.bx, bullet.by, bullet.radius, fill='black')
    
    if not app.player.isAlive:
        drawRect(0, 0, app.width, app.height, fill='black', opacity = 50)
        drawLabel('Game Over', app.width/2, app.height/2, size=64, bold=True,
                  fill='red', align='center')
        drawLabel('Press r to Restart', app.width/2, app.height/2 + 100, 
                  size=28, fill = 'red', bold = True)
        if app.currentWave <= 3:
            drawLabel(f'You only made it to wave {app.currentWave}!' + 
                      ' You suck at this!', 
                      app.width/2, app.height/2 + 50, size=28, bold=True,
                      fill='red', align='center')
        elif app.currentWave > 3 and app.currentWave <= 7:
            drawLabel(f'You made it to wave {app.currentWave}! Good attempt!', 
                      app.width/2, app.height/2 + 50, size=28, bold=True,
                      fill='red', align='center')
        elif app.currentWave > 7 and app.currentWave <= 9:
            drawLabel(f'You made it to wave {app.currentWave}! So close!', 
                      app.width/2, app.height/2 + 50, size=28, bold=True,
                      fill='red', align='center')
        elif app.currentWave == 10:
            drawLabel(f'You made it all the way to wave {app.currentWave}!' +
                       "\n You really couln't close it out?", 
                      app.width/2, app.height/2 + 50, size=28, bold=True,
                      fill='red', align='center')
    
    if app.playerWon:
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 50)
        drawLabel('You win!', app.width/2, app.height/2, size=64, bold=True,
                  fill='lightGreen', align='center')
        drawLabel('Press r to Restart', app.width/2, app.height/2 + 100, 
                  size=28, fill = 'lightGreen', bold = True)
        drawLabel('You made it all the way to wave 10!', 
                  app.width/2, app.height/2 + 60, size=28, bold=True,
                  fill='lightGreen', align='center')

def drawStartScreen(app):
    drawRect(0,0, app.width, app.height, fill = 'lightblue')
    drawLabel('Zombie Apocalypse ', app.width/2, app.height/2 - 300, 
              size = 40, bold = True, fill = 'black')

    buttonWidth = 200
    buttonHeight = 80 
    buttonX = app.width/2 - buttonWidth/2
    buttonY = app.height - 200
    drawRect(buttonX, buttonY, buttonWidth, buttonHeight, 
             fill = 'green', border = 'black')
    drawLabel('Start!', app.width/2, buttonY + buttonHeight/2, 
              size = 30, bold = True, fill = 'black')

    inputWidth = 300
    inputHeight = 50
    inputX = app.width/2 - inputWidth/2
    inputY = buttonY - 100
    drawRect(inputX, inputY, inputWidth, inputHeight, 
             fill = 'white', border = 'black')
    drawLabel('Enter Your Name:', app.width/2, inputY - 30, size = 20, fill = 
              'black')
    drawLabel(app.player.name, app.width/2, inputY + inputHeight/2, 
              size = 20, bold = True, fill = 'black')

    # instructions
    instruction1 = 'Survive 10 grueling waves of zombies!'
    instruction2 = 'Earn money from killing hordes of zombies!'
    instruction3 = 'Upgrade your weaponry to survive!'
    
    instructionX = app.width/2
    instructionY1 = 175
    instructionY2 = 250
    instructionY3 = 325
    drawLabel(instruction1, instructionX, instructionY1, size=24, bold=True)
    drawLabel(instruction2, instructionX, instructionY2, size=24, bold=True)
    drawLabel(instruction3, instructionX, instructionY3, size=24, bold=True)


    
def drawBackground(app):
    drawRect(0, 0, app.width, app.height, fill='silver')

    # draw park grass (top right)
    parkX = app.width - app.buildingWidth
    parkY = 0
    drawRect(parkX, parkY, app.buildingWidth, app.buildingHeight, 
             fill='forestGreen')
    # draw bushes
    bushWidth = 80
    bushHeight = 40
    bush1X = parkX + app.buildingWidth/4
    bush1Y = parkY + app.buildingHeight/4
    drawOval(bush1X, bush1Y, bushWidth, bushHeight, fill = 'green')

    bush2X = app.width - app.buildingWidth/4
    bush2Y = parkY + (3 * app.buildingHeight/4)
    drawOval(bush2X, bush2Y, bushWidth, bushHeight, fill = 'green')

    # draw tree
    trunkX = parkX + app.buildingWidth/2
    trunkY = parkY + app.buildingHeight/2
    trunkWidth = 20
    trunkHeight = 50
    trunkColor = rgb(133, 75, 22)
    drawRect(trunkX, trunkY, trunkWidth, trunkHeight, fill= trunkColor, 
             align = 'center')
    leavesHeight = 70
    leavesWidth = 40
    leavesX = trunkX
    leavesY = trunkY - trunkHeight/2
    drawOval(leavesX, leavesY, leavesWidth, leavesHeight, fill = 'green')

    # draw gun store (top left)
    gunStoreX = 0
    gunStoreY = 0
    gunStoreColor = rgb(64, 67, 84)
    drawRect(gunStoreX, gunStoreY, app.buildingWidth, app.buildingHeight, 
             fill = gunStoreColor)
    
    # draw text for gun store
    gunStoreMessageX = app.buildingWidth/2
    gunStoreMessageY1 = app.buildingHeight/2 
    gunStoreMessageY2 = app.buildingHeight/2 + 25
    gunStoreMessage1 = 'Gun Shop'
    gunStoreMessage2 = "Press 'b'"
    drawLabel(gunStoreMessage1, gunStoreMessageX, gunStoreMessageY1, size=32)
    drawLabel(gunStoreMessage2, gunStoreMessageX, gunStoreMessageY2, size=16)

    # draw armory (bottom right)
    armoryX = app.width - app.buildingWidth
    armoryY = app.height - app.buildingHeight
    drawRect(armoryX, armoryY, app.buildingWidth, app.buildingHeight, 
             fill = 'dimGray')

    # draw text for armory
    armoryMessageX = app.width - app.buildingWidth/2
    armoryMessageY1 = app.height - app.buildingHeight/2 
    armoryMessageY2 = app.height - app.buildingHeight/2 + 25
    armoryMessage1 = 'Armory'
    armoryMessage2 = "Press 'b'"
    drawLabel(armoryMessage1, armoryMessageX, armoryMessageY1, size=32)
    drawLabel(armoryMessage2, armoryMessageX, armoryMessageY2, size=16)

    # draw bottom left building (bottom left)
    leftBuildingX = 0
    leftBuildingY = app.height - app.buildingHeight
    leftBuildingColor = rgb(133, 75, 22)
    drawRect(leftBuildingX, leftBuildingY, app.buildingWidth, 
             app.buildingHeight, fill = leftBuildingColor)

def drawZombie(app, zombie):
    drawRect(zombie.zx, zombie.zy, zombie.width, zombie.height, align='center', 
             fill = 'darkOliveGreen')
    
    pantsColor = rgb(66,40,1)

    # clothes
    zombieClothesX = zombie.zx
    zombieClothesY = zombie.zy + zombie.height/4
    drawRect(zombieClothesX, zombieClothesY, zombie.width, zombie.height/2, 
             align='center', fill=pantsColor)



    # draw health bar
    if zombie.currentHP != zombie.maxHP and zombie.currentHP > 0:
        healthbarHeightAbove = (zombie.height/2 + 10)
        healthbarWidth = 25
        healthbarHeight = 7
        healthbarLength = healthbarWidth * (zombie.currentHP/zombie.maxHP)
        healthbarX = zombie.zx - healthbarWidth/2
        healthbarY = zombie.zy - (zombie.height/2 + 10)
        drawRect(healthbarX, healthbarY, healthbarLength, healthbarHeight, 
                 fill='red')
        drawRect(healthbarX, healthbarY, healthbarWidth, 
                 healthbarHeight, fill=None, border='black')
       
def drawPlayer(app, player):
    drawRect(player.px, player.py, player.width, player.height, 
             align = 'center', fill = 'gold')
    
def drawUI(app):
    # draw healthbar
    healthWidth = app.width/8
    healthHeight = 20
    healthX = app.width - healthWidth - 10
    healthY = 10
    healthLength = healthWidth * (app.player.currentHP/app.player.maxHP)
    if healthLength > 0:
        drawRect(healthX, healthY, healthLength, healthHeight, fill='red')
    drawRect(healthX, healthY, healthWidth, healthHeight, fill=None, 
             border='black')

    # draw shieldbar
    shieldWidth = healthWidth/2
    shieldHeight = healthHeight
    shieldX = healthX + healthWidth/2
    shieldY = healthY + 25
    shieldLength = shieldWidth * (app.player.currentShield/app.player.maxShield)
    if shieldLength > 0:
        drawRect(shieldX, shieldY, shieldLength, shieldHeight, fill='blue')
    drawRect(shieldX, shieldY, shieldWidth, shieldHeight, fill=None, 
             border='black')

    # draw money
    moneyX = 10
    moneyY = 20
    moneyMessage = f'${app.player.money}'
    drawLabel(moneyMessage, moneyX, moneyY, size=32, align='left')

    # draw start button
    if app.inRound == False and app.currentWave == 0:
        startMessage = 'Press to Start Game'
        drawRect(app.startMessageX, app.startMessageY, app.startMessageWidth, 
                 app.startMessageHeight, fill='powderBlue', align='center')
        drawLabel(startMessage, app.startMessageX, app.startMessageY, size=32, 
                  align='center')
        
    # if in round, draw wave number
    if app.inRound:
        waveMessage = f'Wave {app.currentWave}'
        drawLabel(waveMessage, app.startMessageX, app.startMessageY-20, size=32, 
                  align='center')
        

    # draw timer and skip to next wave between rounds
    if app.inRound == False and app.currentWave != 0:
        # timer
        minutes = app.timer // 60
        seconds = app.timer % 60
        if seconds < 10:
            timerMessage = f'{minutes}:0{seconds}'
        else:
            timerMessage = f'{minutes}:{seconds}'
        drawLabel(timerMessage, app.startMessageX, app.startMessageY + 50, 
                  size=32)

        # skip to next wave
        skipMessage = 'Press to Skip to Next Round'
        
        drawRect(app.startMessageX, app.startMessageY, 
                 app.skipMessageWidth, app.startMessageHeight, 
                 fill='crimson', align='center')
        drawLabel(skipMessage, app.startMessageX, app.startMessageY, size=32, 
                  align='center')
        
def drawGunMenu(app):
    # draw background
    drawRect(app.buyMenuBackgroundX, app.buyMenuBackgroundY, app.width * 3/4, 
             app.height * 3/4, 
             fill='lightGray', align='center')
    
    # draw current damage
    currentDamageX = app.buyMenuBackgroundX
    currentDamageY = app.buyMenuBackgroundY - app.buyMenuBackgroundHeight/4
    currentDamage = f'Current Damage: {app.player.damage}'
    drawLabel(currentDamage, currentDamageX, currentDamageY, size=32)

    # draw increase
    increaseDamageX = app.buyMenuBackgroundX
    increaseDamageY = app.buyMenuBackgroundY
    increaseDamage = f'Upgraded Damage: {app.player.damage + app.gunUpgrade}'
    drawLabel(increaseDamage, increaseDamageX, increaseDamageY, size=32)

    # draw buy box
    buyMessage = f'Buy for ${app.gunUpgradeCost}'
    drawRect(app.buyBoxX, app.buyBoxY, app.buyBoxWidth, app.buyBoxHeight, 
             align='center', fill='green')
    drawLabel(buyMessage, app.buyBoxX, app.buyBoxY, size=32)

def drawArmoryMenu(app):
    # draw background
    drawRect(app.buyMenuBackgroundX, app.buyMenuBackgroundY, app.width * 3/4, 
             app.height * 3/4, 
             fill='lightGray', align='center')
    
    # draw current damage
    currentShieldX = app.buyMenuBackgroundX
    currentShieldY = app.buyMenuBackgroundY - app.buyMenuBackgroundHeight/4
    currentShield = (f'Current Shield: {app.player.currentShield}/' + 
                     str(app.player.maxShield))
    drawLabel(currentShield, currentShieldX, currentShieldY, size=32)

    # only draw increase and buy if shield not maxed
    if app.player.currentShield != app.player.maxShield:
        # draw increase
        increaseShieldX = app.buyMenuBackgroundX
        increaseShieldY = app.buyMenuBackgroundY
        upgradedShield = app.player.currentShield + app.shieldUpgrade
        if upgradedShield > app.player.maxShield:
            upgradedShield = app.player.maxShield
        increaseShield = f'Upgraded Shield: {upgradedShield}'
        drawLabel(increaseShield, increaseShieldX, increaseShieldY, size=32)

        # draw buy box
        buyMessage = f'Buy for ${app.shieldUpgradeCost}'
        drawRect(app.buyBoxX, app.buyBoxY, app.buyBoxWidth, app.buyBoxHeight, 
                align='center', fill='green')
        drawLabel(buyMessage, app.buyBoxX, app.buyBoxY, size=32)

def onStep(app):
    if not app.inRound:
        app.player.speed = 6
    if app.inRound:
        app.player.speed = 2 * 1.5
    # move zombies
    if app.currentWave > 0:
        if app.zombies == []:
            app.inRound = False
            #app.currentWave += 1
            app.zombies = getZombiesList(app)
        else:
            if app.inRound:
                for zombie in app.zombies:
                    zombie.moveZombie(app.player) 

    # if not in round, delete all bullets
    if not app.inRound:
        app.bullets = []   
    
    # move bullets and delete if offscreen
    for bullet in app.bullets:
        bullet.bulletMove()
        if bullet.bulletOffScreen(app):
            app.bullets.remove(bullet)
    
    #make the bullets move and then remove once it hits the zombie
    bulletsRemove = []
    for bullet in app.bullets:
        for zombie in app.zombies:
            distance = ((bullet.bx - zombie.zx) ** 2 + 
                        (bullet.by - zombie.zy) ** 2) ** 0.5
            if distance < (zombie.height/2):
                bulletsRemove.append(bullet)
                zombie.currentHP -= app.player.damage
                # if zombie is dead now, remove it from app.zombies
                # also give them the money
                if zombie.currentHP <= 0:
                    app.zombies.remove(zombie)
                    app.player.money += zombie.moneyDropped
                break

    
    for bullet in bulletsRemove:
        if bullet in app.bullets:
            app.bullets.remove(bullet)
            zombie.moveZombie(app.player) 

    # if between rounds, reduce timer
    if not app.inRound and app.currentWave > 0:
        app.numSteps += 1
        if app.numSteps == app.stepsPerSecond:
            app.timer -= 1
            app.numSteps = 0  
        
    # if timer = 0, start next round
    if app.timer <= 0:
        app.inRound = True
        app.timer = 120
    
    if app.currentWave == 10 and app.zombies == []:
        app.playerWon = True

def getZombiesList(app):
    waveNumber = app.currentWave
    zombies = []
    numDefaultZombies = 4 + (2 * waveNumber)
    
    for i in range(numDefaultZombies):
        rX, rY = randomZombieSpawnpoints(app)
        newZombie = Zombie(app, rX, rY)
        zombies.append(newZombie)
       
        newZombie.speed += 0.25 * waveNumber
        newZombie.currentHP += 5 * waveNumber
        newZombie.maxHP += 5 * waveNumber
    return zombies

def randomZombieSpawnpoints(app):
    randomMinimalSpawnValues = list(range(0, 30))
    randomMinimalSpawnValue = choice(randomMinimalSpawnValues)
    randomSpawnValues = list(range(int(app.buildingHeight + 25), 
                                   int(app.width-app.buildingHeight + 1 - 25), 
                                   5))
    randomSpawnValue = choice(randomSpawnValues)
    spawnpoints = [(randomMinimalSpawnValue, randomSpawnValue), 
                   (app.width - randomMinimalSpawnValue, randomSpawnValue), 
                   (randomSpawnValue, randomMinimalSpawnValue), 
                   (randomSpawnValue, app.height-randomMinimalSpawnValue)]
    return choice(spawnpoints)

def onKeyHold(app, keys):

    app.player.movePlayer(app, keys)

def onKeyPress(app, key):
    if 'b' == key:
        if app.gunMenuOpen:
            app.gunMenuOpen = False
        elif app.armoryMenuOpen:
            app.armoryMenuOpen = False
        else:
            # check which of two buy areas they are in
            if (app.player.px <= app.buildingWidth and 
                app.player.py <= app.buildingHeight):
                # in top left so buy guns
                app.gunMenuOpen = True
            elif (app.player.px >= app.width - app.buildingWidth and 
                  app.player.py >= app.height - app.buildingHeight):
                # in bottom right so buy shield
                app.armoryMenuOpen = True
    
    if app.playerWon or not app.player.isAlive:
        if 'r' in key:
            restartGame(app)

    if app.startScreen:
        if key == 'backspace':
            if len(app.player.name) > 0:
                app.player.name = app.player.name[:-1]
        elif ((key.isalpha() or key.isdigit()) and len(app.player.name)< 15 and 
              len(key) == 1):
            app.player.name += key

        
def onMousePress(app, mouseX, mouseY):
    # check if press start game
    if app.startScreen:
        buttonWidth = 200
        buttonHeight = 80
        buttonX = app.width/2 - buttonWidth/2
        buttonY = app.height - 200
        
        if (buttonX <= mouseX <= buttonX + buttonWidth and
            buttonY <= mouseY <= buttonY + buttonHeight):
            if app.player.name != '':
                app.startScreen = False
    
    # check if press on start button
    if app.inRound == False and app.currentWave == 0:
        startLeft = app.startMessageX - app.startMessageWidth/2
        startTop = app.startMessageY - app.startMessageHeight/2
        if pressedButton(app, mouseX, mouseY, startLeft, startTop, 
                              app.startMessageWidth, app.startMessageHeight):
            app.inRound = True
            app.currentWave = 1
    
    if app.inRound:
        bullet = Bullet(app, app.player.px, app.player.py, mouseX, mouseY)
        app.bullets.append(bullet)

    # check if press on skip button
    if app.inRound == False and app.currentWave != 0:
        skipLeft = app.startMessageX - app.skipMessageWidth/2
        skipTop = app.startMessageY - app.startMessageHeight/2
        if pressedButton(app, mouseX, mouseY, skipLeft, skipTop, 
                             app.skipMessageWidth, app.startMessageHeight):
            app.inRound = True
            app.currentWave += 1
            app.player.px, app.player.py = app.width/2, app.height/2
            app.timer = 120

    # if buying gun
    if app.gunMenuOpen:
        buyButtonLeft = app.buyBoxX - app.buyBoxWidth/2
        buyButtonTop = app.buyBoxY - app.buyBoxHeight/2
        if pressedButton(app, mouseX, mouseY, buyButtonLeft, buyButtonTop, 
                         app.buyBoxWidth, app.buyBoxHeight):
            # only let them buy if they have enough money
            if app.player.money >= app.gunUpgradeCost:
                app.player.damage += app.gunUpgrade
                app.player.money -= app.gunUpgradeCost
            

    # if buying shield
    if app.armoryMenuOpen:
        buyButtonLeft = app.buyBoxX - app.buyBoxWidth/2
        buyButtonTop = app.buyBoxY - app.buyBoxHeight/2
        if pressedButton(app, mouseX, mouseY, buyButtonLeft, buyButtonTop, 
                         app.buyBoxWidth, app.buyBoxHeight):
            # only let them buy if they have enough money and not max shield
            upgradedShield = app.player.currentShield + app.shieldUpgrade
            if (app.player.money >= app.shieldUpgradeCost and 
                upgradedShield <= app.player.maxShield):
                # if shield is too close to max, just top off
                # if upgradedShield > app.player.maxShield
                app.player.currentShield = upgradedShield
                app.player.money -= app.shieldUpgradeCost
    
def pressedButton(app, mouseX, mouseY, leftX, topY, width, height):
    rightX = leftX + width
    bottomY = topY + height
    if leftX <= mouseX <= rightX and topY <= mouseY <= bottomY:
        return True
    return False 
    
runApp()