# CODE ADAPTED FROM:
#   - https://pythonprogramming.net/many-blob-objects-intermediate-python-tutorial/
#   - https://github.com/womogenes/GravitySim/blob/main/gravity.pde

# as long as the relative masses are correct I can artificially increase the radius for visibility
# if I scale the masses the same amount that I scale the distances... would it work? 
# no, relative distances between planets are massive

import pygame
import random
import math

FPS = 960
WIDTH = 128
HEIGHT = 128
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
BLACK = (0,0,0)
WHITE = (255,255,255)
G = 0.01 # gravitational constant
dt = 1 # timestep

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

    def __init__(self, pos, vel, radius, mass):
        self.pos = pos
        self.vel = vel
        self.next_pos = pos
        self.next_vel = vel
        self.radius = radius
        self.mass = mass

    def move(self):
        self.pos = self.next_pos
        self.vel = self.next_vel

        self.next_pos.x += self.vel.x
        self.next_pos.y += self.vel.y

        if self.pos.x < 0: self.pos.x = 0
        elif self.pos.x > WIDTH: self.pos.x = WIDTH
        
        if self.pos.y < 0: self.pos.y = 0
        elif self.pos.y > HEIGHT: self.pos.y = HEIGHT

def gravityAcc(pos_a, pos_b, radius, mass):
  dSq = distSquared(pos_a, pos_b);
  if dSq <= (4 * radius * radius):
    return Vector(0, 0)
  return mult(sub(pos_a, pos_b), dt * G * mass / (dSq * math.sqrt(dSq)))

def gravity(bodies):
    for a in bodies:
        for b in bodies:
            if a == b:
                continue
            acc = gravityAcc(b.pos, a.pos, a.radius, a.mass)
            a.next_vel.x += acc.x
            a.next_vel.y += acc.y
    return

def update_physics(bodies):
    gravity(bodies)
    return
    
def main():
    bodies = []
    # for _ in range(10):
    #     pos = Vector(random.randrange(0,WIDTH), random.randrange(0,HEIGHT))
    #     # vel = Vector(random.randrange(-3,3), random.randrange(-3,3))
    #     vel = Vector(0, 0)
    #     bodies.append(Body(pos, vel, random.randrange(0,50)))
    bodies.append(Body(Vector(CENTER_X,CENTER_Y), Vector(0,0), 5, 332950)) # sun
    # bodies.append(Body(Vector(CENTER_X+(0.3871*(400/31)), CENTER_Y), Vector(0,0.03), 1, 0.055)) # mercury
    # bodies.append(Body(Vector(CENTER_X+(0.7223*(400/31)), CENTER_Y), Vector(0,0.03), 1, 0.815)) # venus
    # bodies.append(Body(Vector(CENTER_X+(1*(400/31)), CENTER_Y), Vector(0,0.03), 1, 1)) # earth
    bodies.append(Body(Vector(CENTER_X+60,CENTER_Y), Vector(0,0.03), 2, 8)) # mars
    bodies.append(Body(Vector(CENTER_X+30,CENTER_Y), Vector(0,0.03), 2, 8)) # mars
    # bodies.append(Body(Vector(650,300), Vector(0,0.03), 8, 20)) # jupiter
    # bodies.append(Body(Vector(725,300), Vector(0,0.03), 15, 10)) # saturn
    # bodies.append(Body(Vector(750,300), Vector(0,0.03), 12, 10)) # uranus
    # bodies.append(Body(Vector(775,300), Vector(0,0.03), 12, 10)) # neptune

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_display.fill(WHITE)
        for body in bodies[1:]:
            body.move()
            pygame.draw.circle(game_display, BLACK, [body.pos.x, body.pos.y], body.radius)
        pygame.draw.circle(game_display, BLACK, [bodies[0].pos.x, bodies[0].pos.y], bodies[0].radius)
        update_physics(bodies)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
