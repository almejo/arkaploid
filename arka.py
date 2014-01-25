import pygame
from pygame.locals import *
import gutils
import math
import time
import random
import particle.psystem
import sprites.ball
import sprites.powerup
import sprites.bar
import sprites.android
import sprites.brick
import sound.engine
import engine.mouse
import engine.menu
import engine.keyboard
import engine.animation
import constants
import fonts

from constants import *

 

def draw_text(screen, text, x, y):
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render(str(text) , 1, (255, 0, 0))
        textpos = text.get_rect(centerx = x, centery = y)
        screen.blit(text, textpos)

def create_bricks():
    bricks = pygame.sprite.RenderPlain()
    
    for i in range(0, 17):
        for j in range(3, 5):
            bricks.add(sprites.brick.Brick(i, j, 'brick-green.jpg', (90, 200, 90)))
    for i in range(0, 17):
        for j in range(5, 7):
            bricks.add(sprites.brick.Brick(i, j, 'brick-red.jpg', (200, 90, 90)))
    
    for i in range(0, 17):
        for j in range(7, 8):
            if i % 2 == 0:
                bricks.add(sprites.brick.MetalBrick(i, j, 'brick-metal-3.png', (250, 240, 88)))
            
    for i in range(0, 17):
        for j in range(8, 12):
            bricks.add(sprites.brick.Brick(i, j, 'brick-blue.jpg', (130, 130, 206)))

    for i in range(0, 17):
        for j in range(12, 14):
            bricks.add(sprites.brick.Brick(i, j, 'brick-yellow.png', (250, 240, 88)))

    return bricks

def draw_scanlines(screen):
    for i in range(0, SCREEN_HEIGHT / 2):
        pygame.draw.line(screen, SCANLINES_COLOR, (0, i * 2), (SCREEN_WIDTH, i * 2))

SCANLINES_COLOR = (0, 0, 0)


STATE_PLAYING = 0
STATE_QUIT = 1
STATE_MENU = 2

class StartButton(engine.menu.Button):
    def __init__(self , game, x, y):
        engine.menu.Button.__init__(self, x, y, 'button-start.png', 'button-start-active.png')
        self.game = game
        
    def mouse_click(self, point):
        engine.menu.Button.mouse_click(self, point)
        sound.engine.Manager.play_fx('click-menu')
        time.sleep(1)
        self.game.state = STATE_PLAYING
    def mouse_enter(self, point):
        engine.menu.Button.mouse_enter(self, point)
        #sound.engine.Manager.play_fx('click-menu-activate')

    def mouse_leave(self, point):
        engine.menu.Button.mouse_leave(self, point)
        #sound.engine.Manager.play_fx('click-menu-activate')
        
class QuitButton(engine.menu.Button):
    def __init__(self , game, x, y):
        engine.menu.Button.__init__(self, x, y, 'button-quit.png', 'button-quit-active.png')
        self.game = game
        
    def mouse_click(self, point):
        engine.menu.Button.mouse_click(self, point)
        self.game.state = STATE_QUIT


class Title(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original, self.rect = gutils.load_image('title.png')
        self.time = 0
        self.time_to_end = 2000.0
        self.width  = self.rect.width * 8
        self.height = self.rect.height * 8
        self.speedx = - (self.width - self.rect.width) / self.time_to_end  
        self.speedy = - (self.height - self.rect.height) / self.time_to_end
        self.update(0)
      
        
    def update(self, time):
        self.time += time
        if self.width > self.rect.width:
            self.width += self.speedx * time
            
        if self.height > self.rect.height:
            self.height += self.speedy * time

        self.rect.centerx = (constants.SCREEN_WIDTH) / 2  
        self.rect.centery = 200
        self.image = self.image_original #pygame.transform.scale(self.image_original, (self.width, self.height))
        
        
        
class Level:
    def __init__(self):
        self.balls = pygame.sprite.RenderPlain(sprites.ball.Ball())
        self.bricks = create_bricks()
        self.bars = pygame.sprite.RenderPlain(sprites.bar.Bar(self.balls))
        self.dying_bricks = pygame.sprite.RenderPlain()
    
        self.androids = pygame.sprite.RenderClear()
        self.androids.add(sprites.android.Android(600, 230))
        self.androids.add(sprites.android.Android(690, 230))
        self.androids.add(sprites.android.Android(630, 230))
        self.androids.add(sprites.android.Android(660, 230))
        self.p_systems = []
        
        self.powerups = pygame.sprite.RenderPlain()

class KeyProcesser(engine.keyboard.KeyListener):
    def __init__(self, game):
        self.game = game
        
    def key_pressed(self, key):
        if key == K_p:
           self.game.toggle_pause()
        elif key == K_ESCAPE:
            self.game.state = STATE_QUIT 

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        self.screen = pygame.display.set_mode( (SCREEN_WIDTH,SCREEN_HEIGHT) )
        pygame.display.set_caption( "arka" )
    
        self.state = STATE_MENU
        
        engine.mouse.Manager.init()
        engine.keyboard.Manager.init()

        engine.keyboard.Manager.add_listener(KeyProcesser(self))

        engine.animation.Manager.init('frames.txt', 'animations.txt')
        sound.engine.Manager.load_bg_music('funk', 'Funkorama.ogg')
        #sound.engine.Manager.load_bg_music('menu', 'Funkorama.ogg')
        sound.engine.Manager.start_bg_music('funk')
        sound.engine.Manager.load_effects('effects.txt')
        
        fonts.Manager.init('font-mono.png')
        self.background_image, self.background_rect = gutils.load_image( "back.jpg" )
        self.score = 0
        
        self.game_menu = engine.menu.Menu()  # "background-menu.png")
        self.game_menu.add_button(StartButton(self, 400, 350))
        self.game_menu.add_button(QuitButton(self, 400, 450))
        fonts.Manager.add_text('LEVEL 1', 200, 400, 5000)
        pygame.mouse.set_visible( False )
        self.star = particle.psystem.ParticleImage('star-20.png', 10, 30)
        self.level = Level()
        self.pause = False
        self.pause_frase = fonts.DancingFrase('Pause', 300, 300, -1)
        self.pause_actors = pygame.sprite.RenderClear()
        self.pause_actors.add(sprites.android.Android(600, 500))
        
    def toggle_pause(self):
        self.pause = not self.pause
        sound.engine.Manager.toggle_pause_all()
        if self.pause: pygame.mouse.set_visible(True) 
        else: pygame.mouse.set_visible(False)
        
    def loop(self):
        cursor, cursor_rect = gutils.load_image( "cursor.png", True )
        clock = pygame.time.Clock()
        print self.screen
    
        titles = pygame.sprite.RenderClear(Title())
        self.age = 0
        
        while True:
              time = clock.tick()
              self.age += time
              
              if not self.pause:
                  fonts.Manager.update(time)
              
              if self.state == STATE_MENU:
                  self.game_menu.update(time)
                  pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0,0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))   
                  if self.age > 3000:
                      for title in titles:
                          title.update(time)
                          titles.draw(self.screen)

                  if self.age > 6000: 
                      self.game_menu.draw(self.screen)
                      self.screen.blit( cursor, pygame.mouse.get_pos() )
    
              if self.state == STATE_QUIT:
                  raise SystemExit
              
              elif self.state == STATE_PLAYING:
           
                  if not self.pause:
                      self.update_actors(time)
                                          
                  self.draw()                  
                  
                  if self.pause:
                      self.pause_frase.update(time)
                      self.pause_actors.update(time)
                      draw_scanlines(self.screen)
                      self.pause_frase.draw(self.screen)
                      self.pause_actors.draw(self.screen)
                  
              engine.mouse.Manager.update(time)
              engine.keyboard.Manager.update(time)
              pygame.display.flip()
              if pygame.event.peek(QUIT):
                  self.state = STATE_QUIT
                  
    def update_actors(self, time):
        for android in self.level.androids:
            android.update(time)

        for power in self.level.powerups:
            power.update(time)
            if power.is_dead():
                 self.level.powerups.remove(power)
      
        for system in self.level.p_systems:
              system.update(time)
              if system.is_dead():
                  self.level.p_systems.remove(system) 
    
        for ball in self.level.balls:
            ball.update(time);
            if ball.is_dead():
                self.level.balls.remove(ball)
                if len(self.level.balls) < 1:
                    fonts.Manager.add_text('Game Over!', 200, 400, 1000)
    
        for brick in self.level.dying_bricks:
            brick.update(time)
      
        for bar in self.level.bars:
            bar.update(time)
        
        collisions = pygame.sprite.groupcollide( self.level.balls, self.level.bricks, 0, 0)
        for ball in collisions:
            for brick in collisions[ball]:
                brick.collide(ball)
                if brick.can_die():
                    self.level.bricks.remove(brick)
                    power = sprites.powerup.get_new_powerup()
                    if power is not None:
                        power.set_pos(brick.rect.centerx, brick.rect.centery)
                        self.level.powerups.add(power)
                              
                    self.score += 1
                    x = ball.rect.centerx - ball.old_pos[0]
                    y = ball.rect.centery - ball.old_pos[1]
                    first = False
                    ball.collide(brick)
                    sound.engine.Manager.play_fx('pong')
                    self.level.p_systems.append(particle.psystem.ParticleGroup(40, brick.rect, (x,y), 35,1, 600, 55, brick.color, False, 0.0008))
                    break
  
        collitions = pygame.sprite.groupcollide(self.level.balls, self.level.bars, 0, 0)
        for ball in collitions:
            for bar in collitions[ball]:
                ball.collide_bar(bar)
                sound.engine.Manager.play_fx('ping')
                particles = particle.psystem.ParticleGroup(100, pygame.Rect(ball.rect.left, ball.rect.top + 10,50,5), (-1,-1), 90, 1, 5000, 3, (255,0,0), False, 0.0008)
                particles.set_particle_image(self.star)
                self.level.p_systems.append(particles)
                break
        
        for powerup in pygame.sprite.groupcollide(self.level.powerups, self.level.bars, 1, 0):
            bar.use_power_up(powerup)
            fonts.Manager.add_text('POWERUP!!!!', 300, 50, 3000)
        
        for brick in self.level.dying_bricks:
            if brick.is_dead():
                dying_bricks.remove(brick)

        
    def draw(self):
        self.screen.blit( self.background_image, (0,0) )
                  
        self.level.androids.draw(self.screen)
                       
        self.level.bricks.draw(self.screen)
        self.level.bars.draw(self.screen)
        #dying_bricks.draw(screen)
        
        self.level.balls.draw(self.screen)
        self.level.powerups.draw(self.screen)

        for system in self.level.p_systems:
            system.draw(self.screen)
        
        draw_text(self.screen, "%.8d" % self.score, 650, 180)
        fonts.Manager.draw(self.screen)

                      
if __name__ == '__main__': 
    game = Game()
    game.loop() 
