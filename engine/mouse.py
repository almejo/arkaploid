import pygame
import gutils

STATE_NONE = 0
STATE_MOUSE_DOWN = 1
STATE_MOUSE_UP = 2

class MouseListener:
    def __init__(self):
        self.mouse_in = False
    
class Engine:
    def __init__(self):
        self.time = 0
        self.state = STATE_NONE
        self.last_state = self.state
        self.listeners = []
        self.point_down = (-1,-1)
        self.point_up = (-1, -1)
    
    def init(self):
        print "init mouse"
        
    def add_listener(self, listener):
        self.listeners.append(listener)
    
    def update(self, time):
        self.time += time
            
        buttons = pygame.mouse.get_pressed()
        
        for listener in self.listeners:
            if listener.rect.collidepoint(pygame.mouse.get_pos()):
                if not listener.mouse_in:
                    listener.mouse_enter(pygame.mouse.get_pos())
                    listener.mouse_in = True
            else:
                if listener.mouse_in:
                    listener.mouse_leave(pygame.mouse.get_pos())
                    listener.mouse_in = False
        
        if self.state == STATE_NONE:
            self.last_state = self.state
            if buttons[0]:
                self.state = STATE_MOUSE_DOWN
            else:
                self.state = STATE_MOUSE_UP
        elif self.state == STATE_MOUSE_DOWN:
            if self.state != self.last_state:
                self.point_down = pygame.mouse.get_pos()
                for listener in self.listeners:
                    if listener.rect.collidepoint(self.point_down):
                        listener.mouse_down((self.point_down[0], self.point_down[1]))
                self.last_state = self.state
            if not buttons[0]:
                self.state = STATE_MOUSE_UP
        
        elif self.state == STATE_MOUSE_UP:
            if self.state != self.last_state:
                self.point_up = pygame.mouse.get_pos()
                for listener in self.listeners:
                    if listener.rect.collidepoint(self.point_up):
                        listener.mouse_up((self.point_up[0], self.point_up[1]))
                        if listener.rect.collidepoint(self.point_down):
                            listener.mouse_click((self.point_up[0], self.point_up[1]))
                self.last_state = self.state
            if buttons[0]:
                self.state = STATE_MOUSE_DOWN
        
Manager = Engine()           
