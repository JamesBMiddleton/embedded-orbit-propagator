# CODE ADAPTED FROM:
#   - https://pythonprogramming.net/many-blob-objects-intermediate-python-tutorial/
#   - https://github.com/womogenes/GravitySim/blob/main/gravity.pde

# as long as the relative masses are correct I can artificially increase the radius for visibility
# if I scale the masses the same amount that I scale the distances... would it work? 
# no, relative distances between planets are massive

import pygame
import math
import copy

FPS = 240
WIDTH = 128
HEIGHT = 128
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
BLACK = (0,0,0)
WHITE = (255,255,255)
G = 0.01 # gravitational constant
dt = 1 # timestep
UNIT = 64/32
TRAIL_LENGTH = 6000
RESTITUTION=0.8 # coefficient of restitution when hitting sides

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
        self.pos = [copy.deepcopy(pos)]
        self.vel = vel
        self.next_pos = copy.deepcopy(pos)
        self.next_vel = vel
        self.radius = radius
        self.mass = mass

    def move(self):
        self.pos.insert(0, copy.deepcopy(self.next_pos))
        self.pos = self.pos[:TRAIL_LENGTH]
        self.vel = self.next_vel

        self.next_pos.x += self.vel.x
        self.next_pos.y += self.vel.y

        # if self.next_pos.x < 0: self.vel.x = (-self.vel.x)*RESTITUTION
        # elif self.next_pos.x > WIDTH: self.vel.x = (-self.vel.x)*RESTITUTION
        #
        # if self.next_pos.y < 0: self.vel.y = (-self.vel.y)
        # elif self.next_pos.y > HEIGHT: self.vel.y = (-self.vel.y)


def gravityAcc(pos_a, pos_b, radius, mass):
  dSq = distSquared(pos_a, pos_b);
  if dSq <= (4 * radius * radius):
    return Vector(0, 0)
  return mult(sub(pos_a, pos_b), dt * G * mass / (dSq * math.sqrt(dSq)))

def gravity(bodies):
    for a in bodies:
        for b in bodies[0:1]:
            if a == b:
                continue
            acc = gravityAcc(b.pos[0], a.pos[0], a.radius, a.mass)
            a.next_vel.x += acc.x
            a.next_vel.y += acc.y
    return

def update_physics(bodies):
    gravity(bodies)
    return
    
def main():
    bodies = []

    # earth-moon-s/c system
    bodies.append(Body(Vector(CENTER_X,CENTER_Y), Vector(0,0), 8, 250)) 
    bodies.append(Body(Vector(CENTER_X+12,CENTER_Y), Vector(0,0.03), 2, 1)) 
    bodies.append(Body(Vector(CENTER_X+24,CENTER_Y), Vector(0,0.06), 2, 10)) 
    bodies.append(Body(Vector(CENTER_X+50,CENTER_Y), Vector(0,0.15), 5, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_display.fill(BLACK)
        for body in bodies[1:]:
            body.move()
            for i, trail in enumerate(reversed(body.pos[1:])):
                shade = (((255/TRAIL_LENGTH)*i)/2)+1
                pygame.draw.circle(game_display, (shade, shade, shade), [trail.x, trail.y], 1)
            pygame.draw.circle(game_display, WHITE, [body.pos[0].x, body.pos[0].y], body.radius)
        pygame.draw.circle(game_display, WHITE, [bodies[0].pos[0].x, bodies[0].pos[0].y], bodies[0].radius)
        update_physics(bodies)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
