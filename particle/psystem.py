import math
import pygame
import random
import gutils

class ParticleAnimation:
    def __init__(self, tps, particle_image):
        self.frames = particle_image.frames
        self.frame = 0
        self.age = 0
        self.tps = (random.random() * 3 // 1) * tps + tps
    def update(self, time):
        self.age += time
        if self.age > self.tps: 
            self.frame += 1
            self.age = 0
        if self.frame >= len(self.frames):
            self.frame = 0
            
    def get_frame(self):
        return self.frames[self.frame]

class ParticleImage:
    def __init__(self, filename, angle_steps, size):
        self.original, rect = gutils.load_image(filename, True)
        self.frames = []
        for angle in range(0, 360, angle_steps):
            frame = pygame.transform.rotate(self.original, angle)
            self.frames.append(frame)

class Particle():
    def __init__(self, system, life, centerx, centery, speed, vector, arc, color, change_color ):
        self.age = 0
        self.maxlife = int(random.random() * life * 0.5) + life
        l = vector[0]
        a = math.acos(l) /0.0174532925
        if vector[1] >=0:
            angle =  a
        elif vector[1] < 0:
            angle = 360 - a
         
        self.angle = (int(random.random() * arc) + angle) * 0.0174532925
        self.speed = [math.cos(self.angle), math.sin(self.angle)]
        self.pos = [centerx, centery]
        self.size = int(random.random() * 5) + 1
        self.original_color = color
        self.change_color = change_color
        self.gravity = system.gravity
        self.animation = None
        if system.particle_image is not None:
            self.animation = ParticleAnimation(30, system.particle_image)
        
    def update(self, time):
        self.age += time
        self.pos[0] += self.speed[0] * time / 10
        self.pos[1] += self.speed[1] * time / 10
        
        self.speed[1] += time * self.gravity

        self.speed = [self.speed[0] * 0.999, self.speed[1] * 0.999]

        if self.animation is None:
            if self.change_color:
                self.color = (self.get_color_component(self.original_color[0])
                              , self.get_color_component(self.original_color[1])
                              , self.get_color_component(self.original_color[2]))
            else:
                self.color = self.original_color
        else:
            self.animation.update(time)
        
    def draw(self, surface):
        if self.animation is None:
            pygame.draw.rect(surface, self.color, pygame.Rect(int(self.pos[0]), int(self.pos[1]), self.size, self.size))
        else:
            rect = self.animation.get_frame().get_rect()
            surface.blit(self.animation.get_frame(), (self.pos[0] - rect.width / 2, self.pos[1] - rect.height))

    def get_color_component(self, base):
        return ( base + (self.age) / float(self.maxlife) * (255 - base)  ) % 254

    
class ParticleGroup():
    def __init__(self, lifetime, rect, vector, arc, speed, maxlife, pps, color, change_color, gravity):
        self.rect = pygame.Rect(rect)
        self.arc = arc
        length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1]) 
        self.init_vector = [vector[0] / length , vector[1] / length]
        self.speed = speed
        self.particles = []
        self.maxlife = maxlife
        self.pps = pps
        self.age = 0
        self.sprite = None
        self.lifetime = lifetime
        self.color = color
        self.change_color = change_color
        self.gravity = gravity
        self.particle_image = None
        
    def update(self, time):
        if self.sprite is not None:
            self.rect = pygame.Rect(self.sprite.rect)
            
        self.age += time
        self.emit()
        self.update_particles(time)

    def is_dead(self):
        return self.age > self.lifetime and len(self.particles) == 0

    def emit(self):
        for particle in self.particles:
            if particle.age > particle.maxlife:
                self.particles.remove(particle)
        if self.age > self.lifetime:
            return

        count =  int(random.random() * self.pps)
        for i in range(count):
            x = int(random.random() * self.rect.width) + self.rect.left
            y = int(random.random() * self.rect.height) + self.rect.bottom
            self.particles.append(Particle(self, self.maxlife, x, y, self.speed, self.init_vector, self.arc, self.color, self.change_color))
            
    def update_particles(self, time):
        for particle in self.particles:
            particle.update(time)
            
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
    def set_sprite(self, sprite):
        self.sprite = sprite
        
    def set_particle_image(self, particle_image):
        self.particle_image = particle_image