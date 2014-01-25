import pygame
import gutils
from pygame.locals import *

class KeyListener:
    def key_up(self, key):
        pass
    def key_down(self, key):
        pass
    def key_pressed(self, key):
        pass
    
class Engine:
    def __init__(self):
        self.listeners = []
        self.time = 0 
        self.states = [0] * 323
    
    def init(self):
        keys = pygame.key.get_pressed()
        i = 0
        for key in keys:
            self.states[i] = key
        i += 1 
    
    def add_listener(self, listener):
        self.listeners.append(listener)
        
    def update(self, time):
        self.time += time
        keys = pygame.key.get_pressed()
        i = 0
        for key in keys:
            if self.states[i] != key:
                self.states[i] = key
                if not key: 
                    for listener in self.listeners: 
                        listener.key_up(i)
                        listener.key_pressed(i)
                else:
                    for listener in self.listeners: 
                        listener.key_down(i)
            i += 1  
        
Manager = Engine()