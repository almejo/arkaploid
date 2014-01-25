import pygame
import gutils
import ball
from powerup import *
from constants import *
        
class Bar(pygame.sprite.Sprite):
     def __init__(self, balls):
         pygame.sprite.Sprite.__init__(self)
         self.image, self.rect = gutils.load_image('bar.png', True)
         self.rect.centerx = SCREEN_WIDTH / 2
         self.rect.centery = 580
         self.delta = 0
         self.balls = balls

     def update(self, time):
         self.rect.centerx = max(FIELD_LEFT + self.rect.width / 2 , min(pygame.mouse.get_pos()[0], FIELD_RIGHT - self.rect.width / 2))

     def use_power_up(self, powerup):
         if isinstance(powerup, PowerGreen):
                self.balls.add(ball.Ball())
         else: 
            for b in self.balls:
                b.change_speed(-20)