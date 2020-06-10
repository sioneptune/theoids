import random
import sys
import pygame
import time
from math import cos, sin, tan, acos, atan, sqrt, radians, degrees

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)

wsize = 800 # Size of the window
BOID_SIZE = 5

class Boid:
    
    PERSONAL_SPACE = 25
    VINCINITY = 75
    ANGLE_INCREMENT = 4
    DISTANCE = 1.5
    
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
    
    def move(self, population):
        # print(self.angle)   
        self.choose_next_move(self.boids_in_vincinity(population))
        self.angle = self.next_move
        self.keep_angle_bounds()
        self.x += Boid.DISTANCE * cos(radians(self.angle))
        self.y += Boid.DISTANCE * sin(radians(self.angle))
        self.resolve_oob()
        
    
    def choose_next_move(self, nearby_boids):   
        
        nb_neighbors = len(nearby_boids)
        if nb_neighbors > 0:
            mean_angle = sum([b.angle for b in nearby_boids])/nb_neighbors
            avg_x = sum([b.x for b in nearby_boids])/nb_neighbors
            avg_y = sum([b.y for b in nearby_boids])/nb_neighbors
            too_close = self.boids_too_close(nearby_boids)
        
            if(len(too_close) > 0):
                avg_boid_x = sum([b.x for b in too_close])/len(too_close)
                avg_boid_y = sum([b.y for b in too_close])/len(too_close)
                if self.to_my_left([avg_boid_x, avg_boid_y]):
                    print("It's to my left")
                    self.choose_right()
                else:
                    print("It's to my right")
                    self.choose_left()
        # Avoiding walls        
        if self.y < Boid.VINCINITY: # Near Top
                self.choose_right() if self.to_my_left("TOP") else self.choose_left()
        if wsize - self.y < Boid.VINCINITY:   # Near Bottom
                self.choose_right() if self.to_my_left("BOTTOM") else self.choose_left()
        if self.x < Boid.VINCINITY:   # Near Left
                self.choose_right() if self.to_my_left("LEFT") else self.choose_left()
        if wsize - self.x < Boid.VINCINITY:   # Near Right
                self.choose_right() if self.to_my_left("RIGHT") else self.choose_left()
                
        #print(self.position)
        # print(self.angle)
        return
        
    def resolve_oob(self):
        if self.x < 0:
            self.x = 0
        if self.x > wsize:
            self.y = wsize
        if self.y < 0:
            self.y = 0
        if self.y > wsize:
            self.y = wsize
        
    def to_my_left(self, item):
        if item=="TOP":
            return self.angle < 90 and self.angle > -90
        if item=="BOTTOM":
            return self.angle > 90 or self.angle < -90
        if item=="LEFT":
            return self.angle < 0
        if item=="RIGHT":
            return self.angle > 0
            
        if isinstance(item, list):
            vec_to_pos = [self.x - item[0], self.y - item[1]]
            dir_vec = [cos(radians(self.angle)), sin(radians(self.angle))]
            dot = dir_vec[0]*vec_to_pos[0] + dir_vec[1]*vec_to_pos[1]
            det = dir_vec[0]*vec_to_pos[1] + dir_vec[1]*vec_to_pos[0]
            angle = atan(det/dot)
            return angle > 0
    def choose_left(self):
        self.next_move = self.angle - Boid.ANGLE_INCREMENT
        
    def choose_right(self):
        self.next_move = self.angle + Boid.ANGLE_INCREMENT
       
    def keep_angle_bounds(self):
        if self.angle > 180:
            self.angle -= 360
        if self.angle < -180:
            self.angle += 360
        
    def distance_from(self,boid):
        return ((self.x - boid.x)**2 + (self.y - boid.y)**2)**0.5
    
    def boids_in_vincinity(self, boids):
        return [b for b in boids if self.distance_from(b) <= Boid.VINCINITY and b is not self]
    
    def boids_too_close(self, boids):
        return [b for b in boids if self.distance_from(b) <= Boid.PERSONAL_SPACE and b is not self]
        

def pg_init():
    pygame.init()
    size = (wsize, wsize)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("Lol I kinda tolerate life")
    return screen
    
def run(nb_boids):
    keep_going = True
    clock = pygame.time.Clock()
    screen = pg_init()
    
    boids = [Boid(random.randint(200,600), random.randint(200,600)) for x in range(nb_boids)]  # populate here
    
    while keep_going:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
        
        for boid in boids:
            boid.move(boids)
        
        screen.fill(BLACK)
        for boid in boids:
            box = []
            pygame.draw.ellipse(screen,WHITE,[boid.x - BOID_SIZE/2, boid.y - BOID_SIZE/2, BOID_SIZE, BOID_SIZE])
            
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    
if __name__=="__main__":
    if(len(sys.argv) == 1):
        print("Please specify the number of boids")
    else:
        run(int(sys.argv[1]))
