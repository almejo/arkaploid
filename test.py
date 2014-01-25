import pygame
from pygame.locals import *
import gutils
import time


def main():
 pygame.init()
 pygame.mixer.init()
 sound = gutils.load_sound_file('ping.wav')
 i = 1
 aaa = pygame.mixer.Channel(0)
 while 1:
     time.sleep(3)
     print "play" + str(i)
     aaa.play(sound)
     i += 1
 
 
               
              
if __name__ == '__main__': 
    main()
