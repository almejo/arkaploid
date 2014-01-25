import pygame
import gutils
from pygame.locals import *

class Animation:
    def __init__(self, frames, tb_frames, loop_type):
        self.index = 0
        self.time = 0
        self.frames = frames
        self.frame = frames[0]
        self.loop_type = loop_type
        self.tb_frames = tb_frames
        self.step = 0
        
    def anim(self, time = 0):
        self.time += time
        if self.time > self.tb_frames:
            self.time = 0
            self.step += 1
            if self.step >= len(self.frames):
                self.step = 0;
            self.frame = self.frames[self.step]
        return self.frame
    def get_rect(self):
        return self.frame.get_rect()
    
class Engine:
    def __init__(self):
        self.frames = {}
        self.rects = {}
        self.animations = {}

    def init(self, frame_filename, animation_filename):
        self.read_frames(frame_filename)
        self.read_animations(animation_filename)

    def read_animations(self, filename):
        file = open(filename,'r')
        for line in file.readlines():
            line = line.strip()
            if line[0] == '#' or line.strip == '': continue
            data = line.split(":")
            name = data[0].strip()
            tb_frames = int(data[1].strip())
            loop_type = data[2].strip()
            self.animations[name] = {'frames': self.frames[name]
                                    , 'tb_frames': tb_frames
                                    , 'loop_type': loop_type}
        file.close()

    def get_animation(self, anim_name):
            data = self.animations[anim_name]
            return Animation(data['frames'], data['tb_frames'], data['loop_type'])
            
    def read_frames(self, filename):
        file = open(filename,'r')
        for line in file.readlines():
            line = line.strip()
            if line[0] == '#' or line.strip == '': continue
            data = line.split(":")
            anim_name = data[0].strip()
            sprite_count = int(data[1].strip())
            sprite_file = data[3].strip()
            color_key = data[4].strip() == 'true'
            all_frames, rect = gutils.load_image(sprite_file, color_key)
            
            width = int(data[2].strip())
            height = rect.height
            frames = []
            for i in range(sprite_count):
                surface = pygame.Surface((width, height))
                frames.append(surface)
                surface.blit(all_frames, (0,0), (i * width + i,0, width, height))
                if color_key:
                    surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
             
            self.frames[anim_name] = frames
            self.rects[anim_name] = pygame.Rect(0,0, width, rect.height)
             
        file.close()

AniEngine = Engine()
