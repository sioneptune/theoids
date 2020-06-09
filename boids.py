import random
import pygame
import time
from math import cos, sin, tan, atan, sqrt, radians, degrees

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)

wsize = 800 # Size of the window
BOID_SIZE = 10

class Boid:
    
    PERSONAL_SPACE = 25
    VINCINITY = 75
    ANGLE_INCREMENT = 1
    DISTANCE = 5
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = random.randint(-180,180)
        self.next_move = self.angle
        
    @property
    def position(self):
        return [self.x,self.y]
        
    @position.setter
    def position(self,pos):
        self.x = pos[0]
        self.y = pos[1]
    
    def move(self):
        self.angle = self.next_move
        self.x += Boid.DISTANCE * cos(radians(self.angle))
        self.y += Boid.DISTANCE * sin(radians(self.angle))
    
    def choose_next_move(self, neary_boids):
        #if(self.close_wall() is not None):
        return
        
    def choose_left(self):
        self.next_move = self.angle - Boid.ANGLE_INCREMENT
        
    def choose_right(self):
        self.next_move = self.angle + Boid.ANGLE_INCREMENT
        
    def distance_from(self,boid):
        return ((self.x - boid.x)**2 + (self.y - boid.y)**2)**0.5
    
    def boids_in_vincinity(self, boids):
        return [b for b in boids if self.distance_from(b) <= Boid.VINCINITY and b is not self]
    
    def close_wall(self):
        if self.x < PERSONAL_SPACE:
            return "TOP"
        elif wsize - self.x < PERSONAL_SPACE:
            return "BOTTOM"
        elif self.y < PERSONAL_SPACE:
            return "LEFT"
        elif wsize - self.y < PERSONAL_SPACE:
            return "RIGHT"
        else:
            return None 
        

def pg_init():
    pygame.init()
    size = (wsize, wsize)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("Lol I kinda tolerate life")
    return screen
    
def run():
    keep_going = True
    clock = pygame.time.Clock()
    screen = pg_init()
    
    boids = [Boid(400,400)]  # populate here
    
    while keep_going:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
        
        for boid in boids:
            boid.move()
        
        screen.fill(BLACK)
        for boid in boids:
            box = []
            pygame.draw.ellipse(screen,WHITE,[boid.x - BOID_SIZE/2, boid.y - BOID_SIZE/2, BOID_SIZE, BOID_SIZE])
            
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    
run()
