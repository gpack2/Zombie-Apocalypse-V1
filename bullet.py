from cmu_graphics import *

class Bullet:
    def __init__(self, app, startX, startY, targetX, targetY):
        self.bx = startX
        self.by = startY
        self.speed = 5
        self. radius = 5

        dx = targetX - startX
        dy = targetY - startY
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0:
            distance = 1
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed

    def bulletMove(self):
        self.bx += self.vx
        self.by += self.vy
        
    def bulletOffScreen(self, app):
        return ((self.bx < 0 or self.bx > app.width) or 
            (self.by < 0 or self.by > app.height))
            

