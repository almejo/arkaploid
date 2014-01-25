import pygame, os
from pygame.locals import *

IMAGES_DIR = "images"
SOUND_DIR = "sound"
def load_image(name, colorkey = False):
    fullname = os.path.join(IMAGES_DIR, name)

    try: image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'No se puede cargar la imagen: ', fullname
        raise SystemExit, message

    image = image.convert()
    if(colorkey):
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound_file(name):

    class NoneSound:
        def play(self): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(SOUND_DIR, name)

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "No se pudo cargar el sonido:", fullname
        raise SystemExit, message

    return sound
