from cmu_graphics import *

class Player():
    def __init__(self, app):
        self.name = ''
        self.px, self.py = app.width/2, app.height/2
        self.width = 20
        self.height = 50
        self.money = 0
        self.isAlive = True
        self.currentHP = 1000
        self.maxHP = 1000
        self.maxShield = 500
        self.currentShield = 0
        self.speed = 2 * 1.5
        self.damage = 25

    def isLegalMove(dx, dy):
        return True
    
    def movePlayer(self, app, keys):
        dx = 0
        dy = 0
        if 'left' in keys or 'a' in keys:
            dx += -1 * self.speed
            dy += 0
        if 'right' in keys or 'd' in keys:
            dx += 1 * self.speed
            dy += 0
        if 'up' in keys or 'w' in keys:
            dx += 0
            dy += -1 * self.speed
        if 'down' in keys or 's' in keys:
            dx += 0
            dy += 1 * self.speed
        
        #new position
        newPx = self.px + dx
        newPy = self.py + dy

        collision = False
        #player dimensions
        playerLeft = newPx - self.width/2
        playerRight = newPx + self.width/2
        playerTop = newPy - self.height/2
        playerBottom = newPy + self.height/2

        #building dimensions
        buildingLeft = 0
        buildingRight = app.buildingWidth
        buildingTop = app.height - app.buildingHeight 
        buildingBottom = app.height
        #Check collision
        collision = False
        #get coordinates for corner stores
        buildings = [(0,0,app.buildingWidth, app.buildingHeight),
                    (0, app.height - app.buildingHeight, 
                     app.buildingWidth, app.height),
                    (app.width - app.buildingWidth, 
                     app.height - app.buildingHeight, app.width, app.height)
                    ]
        
        # check if collision only with bottom left
        bottomLeftCollision = False
        bottomLeftBuilding = [(0, app.height - app.buildingHeight, 
                               app.buildingWidth, app.height)]
        for left, top, right, bottom in bottomLeftBuilding:
            if (playerRight > left and playerLeft < right
                and playerBottom > top and playerTop < bottom):
                    bottomLeftCollision = True
                    break 
            
        #loop through each element in list check conditions
        for left, top, right, bottom in buildings:
            if (playerRight > left and playerLeft < right
                and playerBottom > top and playerTop < bottom):
                    collision = True
                    break

        
        # in a round, can't go in any building
        if not collision and self.isAlive and app.inRound:
            #if Player.isLegalMove(dx, dy):
            self.px += dx
            self.py += dy

        # not in a round, can't go in bottom left only
        if not bottomLeftCollision and self.isAlive and not app.inRound:
            #if Player.isLegalMove(dx, dy):
            self.px += dx
            self.py += dy





