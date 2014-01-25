import pygame
import gutils
from pygame.locals import *
import engine.animation
import random

class Android(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #frames, rect = gutils.load_image('android.png', True)
        #self.frames = []
        #for i in range(8):
        #     self.frames.append(pygame.Surface((24, 41)))
             
        #for i in range(8):
        #    self.frames[i].blit(frames, (0,0), (i * 24 + i,0,24,41))
        #    colorkey = self.frames[i].get_at((0,0))
        #    self.frames[i].set_colorkey(colorkey, RLEACCEL)
        self.rect = pygame.Rect(0,0,24,41)
        self.rect.centerx, self.rect.centery = x, y
        #self.image = self.frames[0]
        #self.age = 0
        #self.step = 0
        self.ani = engine.animation.Manager.get_animation('android_left')
        self.image = self.ani.anim(random.random() * 5 * 20)
        
    
    def update(self, time):
        self.image = self.ani.anim(time)