import pygame
import engine.mouse
import gutils
import constants
import math

class Manager:
    def __init__(self):
        self.menus = []
        
    def add_menu(self, menu):
        self.menus.append(menu)
        
    def update(self, time):
        for menu in self.menus:
            menu.update(time)
    
    def draw(self, screen):
        for menu in self.menus:
            menu.draw(screen)
            
class Menu:
    def __init__(self, filename = None):
        self.buttons = pygame.sprite.RenderPlain()
        self.background = None
        if filename is not None:
            self.background, rect = gutils.load_image(filename)
        self.background_color = None

    def set_background_color(self, color):
        self.background_color = color
        
    def add_button(self, button):
        self.buttons.add(button)
        
        
    def update(self, time):
        for button in self.buttons:
            button.update(time)
            
    def draw(self, screen):

        if self.background is not None:
            screen.blit(self.background, (0, 0))
    
        if self.background_color is not None:
            pygame.draw.rect(screen, self.background_color, pygame.Rect(0,0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
                             
        self.buttons.draw(screen)
        
class Button(pygame.sprite.Sprite, engine.mouse.MouseListener):
    def __init__(self,x, y, filename, filename2):
        pygame.sprite.Sprite.__init__(self)
        engine.mouse.MouseListener.__init__(self)
        self.image1, self.rect1 = gutils.load_image(filename, True)
        self.image2, self.rect2 = gutils.load_image(filename2, True)
        self.rect = self.rect1
        self.image = self.image1
        self.rect.centerx = self.rect2.centerx = self.x = x
        self.rect.centery = self.rect2.centery = self.y = y
        engine.mouse.Manager.add_listener(self)
        self.time = 0
        self.active = False
        
    def update(self, time):
        if self.active:
            self.time += time
            self.rect.centery = self.y + math.cos(self.time * 3.14 / 500.0) * 10
        else:
            self.time = 0
            self.rect.centery = self.y
            
    def mouse_down(self, point):
        pass
    def mouse_up(self, point):
        pass
        
    def mouse_click(self, point):
        pass
        
    def mouse_enter(self, point):
        self.image = self.image2
        self.rect = self.rect2
        self.active = True
        pass
        
    def mouse_leave(self, point):
        pass
        self.active = False
        self.image = self.image1
        self.rec = self.rect1
        