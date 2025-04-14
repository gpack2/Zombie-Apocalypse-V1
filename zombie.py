from cmu_graphics import *

class Zombie():

    def __init__(self, app, zx, zy):
        self.zx = zx
        self.zy = zy
        self.maxHP = 100
        self.currentHP = self.maxHP
        self.damage = 20
        self.speed = 1 #pixel per second
        self.radius = 20
        self.alive = True
        self.width = 20
        self.height = 50
        self.useless = app.width
        self.moneyDropped = 10
        self.isStepping = False
    

    def moveZombie(self, player):
        # switch legs for walking
        self.isStepping = True if self.isStepping == False else False

        if self.alive and player.isAlive:
            dx = player.px - self.zx
            dy = player.py - self.zy

            distance = (dx**2 + dy**2) ** 0.5
            if distance == 0:
                return
            
            dx = self.speed * dx / distance
            dy = self.speed * dy / distance
            if self.collidesWithPlayer(player, dx, dy):
                self.attackPlayer(player)
                return
            
            if self.zombieIsLegalMove(dx, dy):
                self.zx += dx
                self.zy += dy
            # Try horizontal only
            elif self.zombieIsLegalMove(dx, 0):
                self.zx += dx
            # Try vertical only
            elif self.zombieIsLegalMove(0, dy):
                self.zy += dy
    
    def zombieIsLegalMove(self, dx, dy):
        if (self.collidesWithTopLeftBuilding(dx, dy) or
            self.collidesWithBotLeftBuilding(dx, dy) or
            self.collidesWithBotRightBuilding(dx, dy) or
            self.collidesWithPlayer(app.player, dx, dy) or
            self.collidesWithZombie(app, dx, dy)):
            return False
        return True
    
    def collidesWithTopLeftBuilding(self, dx, dy):
        buildingLeft = 0
        buildingTop = 0
        buildingRight = app.buildingWidth
        buildingBottom = app.buildingHeight
        nextZx = self.zx + dx
        nextZy = self.zy + dy
        if (nextZx - self.radius < buildingRight and
            nextZx + self.radius > buildingLeft and
            nextZy - self.radius < buildingBottom and
            nextZy + self.radius > buildingTop):
            return True
        return False
    
    def collidesWithBotLeftBuilding(self, dx, dy):
        buildingLeft = 0
        buildingBottom = app.height
        buildingTop = app.height - app.buildingHeight
        buildingRight = app.buildingWidth
        nextZx = self.zx + dx
        nextZy = self.zy + dy
        if (nextZx - self.radius < buildingRight and
            nextZx + self.radius > buildingLeft and
            nextZy - self.radius < buildingBottom and
            nextZy + self.radius > buildingTop):
            return True
        return False
    
    def collidesWithBotRightBuilding(self, dx, dy):
        buildingLeft = app.width - app.buildingWidth
        buildingBottom = app.height
        buildingTop = app.height - app.buildingHeight
        buildingRight = app.width
        nextZx = self.zx + dx
        nextZy = self.zy + dy
        if (nextZx - self.radius < buildingRight and
            nextZx + self.radius > buildingLeft and
            nextZy - self.radius < buildingBottom and
            nextZy + self.radius > buildingTop):
            return True
        return False
    
    def collidesWithZombie(self, app, dx, dy):
        # nextZx = self.zx + dx
        # nextZy = self.zy + dy

        # (zombieLeft, 
        #  zombieRight, 
        #  zombieTop, 
        #  zombieBottom) = self.getZombieHitbox(nextZx, nextZy)

        # for other in app.zombies:
        #     if other is self or not other.alive:
        #         continue

        #     otherLeft = other.zx - other.width / 2
        #     otherRight = other.zx + other.width / 2
        #     otherTop = other.zy - other.height / 2
        #     otherBottom = other.zy + other.height / 2

        #     if (zombieRight > otherLeft and zombieLeft < otherRight and
        #         zombieBottom > otherTop and zombieTop < otherBottom):
        #         return True
        return False
        
    
    def getZombieHitbox(self, nextZx, nextZy):
        zombieLeft = nextZx - self.width / 2
        zombieRight = nextZx + self.width / 2
        zombieTop = nextZy - self.height / 2
        zombieBottom = nextZy + self.height / 2
        return (zombieLeft, zombieRight, zombieTop, zombieBottom)

    def collidesWithPlayer(self, player, dx, dy):
        nextZx = self.zx + dx
        nextZy = self.zy + dy

        (zombieLeft, 
         zombieRight, 
         zombieTop, 
         zombieBottom) = self.getZombieHitbox(nextZx, nextZy)

        playerLeft = player.px - player.width / 2
        playerRight = player.px + player.width / 2
        playerTop = player.py - player.height / 2
        playerBottom = player.py + player.height / 2

        if (zombieRight > playerLeft and zombieLeft < playerRight and
            zombieBottom > playerTop and zombieTop < playerBottom):
            return True
        return False
    
    def attackPlayer(self, player):
        if player.currentShield > 0 and player.currentShield > self.damage:
            player.currentShield -= self.damage
        elif player.currentShield > 0 and player.currentShield <= self.damage:
            player.currentShield = 0
            player.currentHP -= self.damage - player.currentShield
        else:
            player.currentHP -= self.damage
        if player.currentHP <= 0:
            player.isAlive = False
    pass

class FastZombie(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, speed=2.0, health=50, damage=5, reward=10)
