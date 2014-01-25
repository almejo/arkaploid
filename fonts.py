import pygame
from pygame.locals import *
import gutils
import math
import random

class FontEngine:
    def __init__(self):
        self.letters = {}
        self.fraces = []
    
    def init(self, filename):
        image_all, rect = gutils.load_image(filename)
        self.read_line(image_all, 'ABCDEFGHIJKLMNOPQRSTUVWXYXz', 30, 60, 0)
        self.read_line(image_all, 'abcdefghijklmnopqrstuvwxyz', 30, 60, 60)
        self.read_line(image_all, '1234567890', 30, 60, 120)
        self.read_line(image_all, '!@#$%^&*()[]{}"\',.', 30, 60, 180)
        
    def read_line(self, image, letters, width, height, offset ):
        i = 0
        for letter in letters:
            surface = pygame.Surface((width, height))
            surface.blit(image, (0, 0), (i * width, offset, width, height))
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
            self.letters[letter] = surface
            i += 1
    
    def p(self, screen):
        i = 0
        for letter in self.letters:
            screen.blit(self.letters[letter], (30 * i, 100))
            i += 1
            
    def get_letter(self, letter):
        return self.letters[letter]

    def add_text(self, text, x, y, time):
        frase = DancingFrase(text, x, y, time)
        self.fraces.append(frase)
        return frase
    
    def remove_text(self, frase):
        self.fraces.remove(frase)
        
    def update(self, time):
        for frase in self.fraces:
            frase.update(time)
            if frase.is_dead():
                self.fraces.remove(frase)
            
    def draw(self, screen):
        for frase in self.fraces:
            frase.draw(screen)

class DancingLetter:
    def __init__(self, letter, original_x, original_y, delta):
        self.original_y = original_y
        self.delta = delta
        self.x = original_x
        self.y = original_y
        self.time = 0
        self.speed = 0.1
        if letter != ' ':
            self.letter = Manager.get_letter(letter)
        else: 
            self.letter = None
    
    def update(self, time):
        self.time += time
        #self.y = self.original_y + math.cos((self.delta + self.time) * 3.14 / 500.0) * 10 - self.speed * self.time 
        self.y = self.original_y + math.cos((self.delta + self.time) * 3.14 / 500.0) * 10
        
    def draw(self, screen):
        if self.letter is not None:
            screen.blit(self.letter, (self.x, self.y))
    
class DancingFrase:
    def __init__(self, frase, x, y, time):
        self.letters = []
        self.maxtime = time
        self.time = 0
        i = 0
        for letter in frase:
            self.letters.append(DancingLetter(letter, x + i * 30, y, 100 * i))
            i += 1
            
    def update(self, time):
        self.time += time
        for letter in self.letters:
            letter.update(time)
            
    def is_dead(self):
        return self.maxtime > 0 and self.time > self.maxtime
    
    def draw(self, screen):
        for letter in self.letters:
            letter.draw(screen)
        
        
Manager = FontEngine()