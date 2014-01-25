import pygame
import gutils
from constants import *

DEFAULT_SPEED = 0.2

class Ball(pygame.sprite.Sprite):
     def __init__(self):
         pygame.sprite.Sprite.__init__(self)
         self.age = 0
         self.image, self.rect = gutils.load_image('ball.gif', True)
         self.rect.centerx = 0
         self.rect.centery = 550
         self.old_pos = [self.rect.centerx, self.rect.centery]
         self.speed = [1, -1]
         self.set_speed(DEFAULT_SPEED)
         self.delta = 0

     def update(self, time):
         self.age += time
         if self.rect.left <= FIELD_LEFT or self.rect.right >= FIELD_RIGHT:
             self.speed[0] = -self.speed[0]
         #if self.rect.top <= FIELD_BOTTOM or self.rect.bottom >= FIELD_TOP:
         #    self.speed[1] = -self.speed[1]
         if self.rect.top <= FIELD_BOTTOM:
             self.speed[1] = -self.speed[1]
        
         if self.old_pos[0] != self.rect.centerx or self.old_pos[1] != self.rect.centery:
             self.old_pos = [self.rect.centerx, self.rect.centery]
        
         self.rect.centerx += self.speed[0] * time;
         self.rect.centery += self.speed[1] * time;
         
         m = min(self.rect.centerx, FIELD_RIGHT - self.rect.width / 2)
         self.rect.centerx = max(self.rect.width / 2 + FIELD_LEFT, m)
         #self.rect.centery = max(self.rect.height / 2 + FIELD_BOTTOM, min(self.rect.centery, FIELD_TOP - self.rect.height / 2))
         self.rect.centery = max(self.rect.height / 2 + FIELD_BOTTOM, self.rect.centery)
         
         self.delta = time
         if self.age > 30000: self.set_speed(DEFAULT_SPEED)
         
     def collide(self, brick):
         self.rect.centerx -= self.speed[0] * self.delta;
         self.rect.centery -= self.speed[1] * self.delta;
         
         if brick.rect.top < self.rect.bottom or brick.rect.bottom > self.rect.top:
            self.speed[1] = -self.speed[1]
         if brick.rect.left > self.rect.right or brick.rect.right < self.rect.left:
            self.speed[0] = -self.speed[0]
            
     def collide_bar(self, bar):
         self.rect.centery = bar.rect.top - self.rect.height / 2 - 1
         self.speed[1] = -self.speed[1]
     
     def change_speed(self, delta):
         self.speed[0] *= (100 + delta) / 100.0
         self.speed[1] *= (100 + delta) / 100.0
    
     def set_speed(self, speed):
         self.age = 0
         self.speed[0] = self.speed[0] / abs(self.speed[0]) * speed
         self.speed[1] = self.speed[1] / abs(self.speed[1]) * speed
         
     def is_dead(self):
         return self.rect.top > SCREEN_HEIGHT  