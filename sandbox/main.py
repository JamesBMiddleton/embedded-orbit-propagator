# CODE ADAPTED FROM https://pythonprogramming.net/many-blob-objects-intermediate-python-tutorial/

import pygame
import random
import math

FPS = 240
WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
G = 0.01 # gravitational constant
dt = 1 # timestep
r = 2 # ?

# --- HELPERS ---

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distSquared(a, b):
  return (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)

def sub(a, b):
  return Vector(a.x - b.x, a.y - b.y)

def add(a, b):
  return Vector(a.x + b.x, a.y + b.y)

def mult(a, scalar):
  return Vector(a.x * scalar, a.y * scalar)

# ---------------

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Propagation")
clock = pygame.time.Clock()

class Body:

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.next_pos = pos
        self.next_vel = vel
        self.size = random.randrange(4,50)

    def move(self):
        self.pos = self.next_pos
        self.vel = self.next_vel

        self.next_pos.x += self.vel.x
        self.next_pos.y += self.vel.y

        if self.pos.x < 0: self.pos.x = 0
        elif self.pos.x > WIDTH: self.pos.x = WIDTH
        
        if self.pos.y < 0: self.pos.y = 0
        elif self.pos.y > HEIGHT: self.pos.y = HEIGHT

def gravityAcc(pos_a, pos_b, mass):
  dSq = distSquared(pos_a, pos_b);
  if dSq <= (4 * r * r):
    return Vector(0, 0)
  return mult(sub(pos_a, pos_b), dt * G * mass / (dSq * math.sqrt(dSq)))

def gravity(bodies):
    for a in bodies:
        for b in bodies:
            if a == b:
                continue
            acc = gravityAcc(b.pos, a.pos, a.size)
            a.next_vel.x += acc.x
            a.next_vel.y += acc.y
    return

def update_physics(bodies):
    gravity(bodies)
    return
    
def main():
    bodies = []
    for _ in range(10):
        pos = Vector(random.randrange(0,WIDTH), random.randrange(0,HEIGHT))
        # vel = Vector(random.randrange(-3,3), random.randrange(-3,3))
        vel = Vector(0, 0)
        bodies.append(Body(pos, vel))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_display.fill(WHITE)
        for body in bodies:
            body.move()
            pygame.draw.circle(game_display, BLACK, [body.pos.x, body.pos.y], body.size)
        update_physics(bodies)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
