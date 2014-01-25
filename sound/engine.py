import pygame
import gutils

class SoundManager:
    def __init__(self, on):
        self.bg_music = {}
        self.pause = False
        self.age = 0
        self.on = on
        self.effects = {}
        self.current_bg_music = None
       
        #pygame.mixer.init(44100, -16, 2, 512)
        #self.channel = pygame.mixer.Channel(0)
        
    def load_effects(self, filename):
        
        if not self.on: return
        
        file = open('effects.txt','r')
        for line in file.readlines():
            line = line.strip()
            if line[0] == '#' or line.strip == '': continue
            data = line.split(":")
            name = data[0].strip()
            file = data[1].strip()
            self.effects[name] = gutils.load_sound_file(file)
            
    def play_fx(self, name):
        if not self.on: return
        
        fx = self.effects[name]
        #self.channel.play(fx)
        fx.play()
    
    def load_bg_music(self, key, file):
        if not self.on:
            return
        
        self.bg_music[key] = gutils.load_sound_file(file)
        
    def start_bg_music(self, key):
        if not self.on:
            return 
        
        #self.bg_state = BG_STARTING
        if self.current_bg_music is not None:
            self.current_bg_music.stop()
            
        self.current_bg_music = self.bg_music[key]
        self.bg_music[key].play()
    
    def update(self, time):
        self.age += time

    def toggle_pause_all(self):
        if not self.on: return
        
        self.pause = not self.pause
        
        
        if self.bg_music is not None:
            if self.pause:
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()
                
Manager = SoundManager(True)