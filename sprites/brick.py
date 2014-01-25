import pygame
import gutils
from pygame.locals import *
import random
from constants import *

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image, self.rect = gutils.load_image(filename, 0)
        self.rect.left = x * self.rect.width + FIELD_LEFT
        self.rect.centery = y * self.rect.height + (self.rect.height / 2)
        self.pos = [self.rect.centerx, self.rect.centery]
        self.time = 0
        self.state = BRICK_STATE_NONE
    def update(self, time):
        if self.state == BRICK_STATE_DYING:
           self.pos[0] += self.speed[0] * time;
           self.pos[1] += self.speed[1] * time;
           self.time += time;
           self.update_center()
           self.delta = time
           
    def collide(self, ball):
        if self.state == BRICK_STATE_NONE:
            self.state = BRICK_STATE_DYING
            self.speed = [ball.speed[0], ball.speed[1]]
            
    def is_dead(self):
        return self.state == BRICK_STATE_DYING and self.time > 1000
 
    def update_center(self):
         self.rect.centerx = self.pos[0];
         self.rect.centery = self.pos[1];

    def can_die(self):
        return True
    
class MetalBrick(Brick):
    def __init__(self, x, y, filename, color):
        Brick.__init__(self, x, y, filename, color)
        
    def can_die(self):
        return False