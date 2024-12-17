import pygame as py
import math

class Ball (py.sprite.Sprite):
    
    speedx = 2
    speedy = 1
    gravity = -9.81
    one_meter = 10
    
    def __init__(self, x, y):
        super().__init__()
        self.image = py.Surface((14, 14), py.SRCALPHA)
        py.draw.circle(self.image, (0, 0, 0), (7, 7), 7)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        
    

    def update(self, velocity, angle, tick):
        
        angle_radians = math.radians(angle)
        velocity_x = math.cos(angle_radians) * velocity
        velocity_y = math.sin(angle_radians) * velocity

        time_in_seconds = tick/60
        
        distance = self.x + (velocity_x * time_in_seconds) * self.one_meter
        height = self.y - ( velocity_y * time_in_seconds + (self.gravity * time_in_seconds**2)/2) * self.one_meter

        if (height<self.y or tick==0):
            self.rect.centerx = math.floor(distance)
            self.rect.centery = math.floor(height)

            return (self.rect.centerx, self.rect.centery, False)
        else: 
            self.rect.centery = self.y
            return (self.rect.centerx, self.y, True)