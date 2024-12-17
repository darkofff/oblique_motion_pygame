import pygame as py
import math

class Ball (py.sprite.Sprite):

    
    def __init__(self, x, y, GRAVITY):
        super().__init__()
        self.image = py.Surface((14, 14), py.SRCALPHA)
        py.draw.circle(self.image, (0, 0, 0), (7, 7), 7)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.gravity = GRAVITY
       
        
    

    def update(self, velocity, angle, tick, meter_size):

        one_meter = int(meter_size)
        
        angle_radians = math.radians(angle)
        velocity_x = math.cos(angle_radians) * velocity
        velocity_y = math.sin(angle_radians) * velocity

        time_in_seconds = tick/60
        
        distance = self.x + (velocity_x * time_in_seconds) * one_meter
        height = self.y - ( velocity_y * time_in_seconds + (self.gravity * time_in_seconds**2)/2) * one_meter

        if (height<self.y or tick==0):
            self.rect.centerx = math.floor(distance)
            self.rect.centery = math.floor(height)

            return (self.rect.centerx, self.rect.centery, False, (velocity_x, velocity_y))
        else: 
            self.rect.centery = self.y
            return (self.rect.centerx, self.y, True, (velocity_x, velocity_y))