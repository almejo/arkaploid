import pygame
import gutils
from pygame.locals import *
import engine.animation
import random
from constants import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speedy = (random.random() * 2 + 1) / 10
        self.age = 0
        pass
    
    def update(self, time):
        self.rect.centery += time * self.speedy
        self.age += time
    def set_pos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        
    def is_dead(self):
        return self.rect.top > SCREEN_HEIGHT
    
class SlowBall(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.animation = engine.animation.Manager.get_animation('power_red')
        self.image = self.animation.anim()
        self.rect = self.animation.get_rect()
        
    def update(self, time):
        PowerUp.update(self, time)
        self.image = self.animation.anim(time)
        
        
class PowerGreen(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.animation = engine.animation.Manager.get_animation('power_green')
        self.image = self.animation.anim()
        self.rect = self.animation.get_rect()
        
    def update(self, time):
        PowerUp.update(self, time)
        self.image = self.animation.anim(time)
    
def get_new_powerup():
    prob = random.random() * 100
    if prob > 20:
        return
    if prob > 10:
         return SlowBall()
    return PowerGreen()