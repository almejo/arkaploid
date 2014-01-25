import pygame
import gutils
import particle.psystem
from pygame.locals import *

def game():
    pygame.init()
    screen = pygame.display.set_mode( (800,600) )
    pygame.display.set_caption( "arka" )
    clock = pygame.time.Clock()

    star, r = gutils.load_image('star.png');
    background_image, background_rect = gutils.load_image( "back.jpg" )
    angle = 0
    p = particle.psystem.ParticleImage('star.png', 10, 30)
    print p
    particles = particle.psystem.ParticleGroup(400000, pygame.Rect(300,300, 50,50), (-1,-1), 90,1, 10000, 2, (255,0,0), False, 0.0008)
    particles.set_particle_image(p)
    
    while True:
        time = clock.tick()
        particles.update(time)
        
        angle += time * 0.2
        if angle >= 360: angle = 0
        
        star2 = pygame.transform.rotate(star, angle)
        keyinput = pygame.key.get_pressed()
        screen.blit( background_image, (0,0) )                  
        screen.blit( star, (100,100) )
        rect = star2.get_rect()                  
        screen.blit( star2, (150 - rect.width/2,100  - rect.height/2 ) )                  
      
        i= 0
        for frame in p.frames:
            screen.blit(frame, (100 + i * 35, 300))
            i +=1
      
        particles.draw(screen)
        pygame.display.flip()
        if keyinput[K_ESCAPE] or pygame.event.peek(QUIT):
            raise SystemExit
  
if __name__ == '__main__': 
    game()
