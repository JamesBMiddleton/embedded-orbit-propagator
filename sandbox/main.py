# CODE ADAPTED FROM:
#   - https://pythonprogramming.net/many-blob-objects-intermediate-python-tutorial/
#   - https://github.com/womogenes/GravitySim/blob/main/gravity.pde

# as long as the relative masses are correct I can artificially increase the radius for visibility
# if I scale the masses the same amount that I scale the distances... would it work? 
# no, relative distances between planets are massive

import pygame
import math
import copy

FPS = 480
WIDTH = 128
HEIGHT = 128
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
BLACK = (0,0,0)
WHITE = (255,255,255)
G = 0.01 # gravitational constant
dt = 1 # timestep
UNIT = 64/32
TRAIL_LENGTH = 1000
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

        if self.next_pos.x < 0: self.vel.x = (-self.vel.x)*RESTITUTION
        elif self.next_pos.x > WIDTH: self.vel.x = (-self.vel.x)*RESTITUTION

        if self.next_pos.y < 0: self.vel.y = (-self.vel.y)
        elif self.next_pos.y > HEIGHT: self.vel.y = (-self.vel.y)


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
            acc = gravityAcc(b.pos[0], a.pos[0], a.radius, a.mass)
            a.next_vel.x += acc.x
            a.next_vel.y += acc.y
    return

def update_physics(bodies):
    gravity(bodies)
    return
    
def main():
    bodies = []
    
    # chaotic 3 body system
    bodies.append(Body(Vector(CENTER_X,CENTER_Y+21), Vector(0,0.1), 5, 25)) 
    bodies.append(Body(Vector(CENTER_X+24,CENTER_Y-10), Vector(0,-0.1), 5, 25)) 
    bodies.append(Body(Vector(CENTER_X-23,CENTER_Y-10), Vector(0,0), 5, 25))

    # pygame.font.init()
    # font = pygame.font.SysFont('Comic Sans MS', 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_display.fill(BLACK)
        for body in bodies:
            body.move()
            for i, trail in enumerate(reversed(body.pos)):
                radius=(body.radius/TRAIL_LENGTH)*i
                shade = (255/TRAIL_LENGTH)*i
                pygame.draw.circle(game_display, (shade, shade, shade), [trail.x, trail.y], radius)
        # text_surface = font.render('James Middleton', False, (255, 255, 255))
        # game_display.blit(text_surface, (CENTER_X-50,CENTER_Y-20))
        # text_surface = font.render('Software Engineer', False, (255, 255, 255))
        # game_display.blit(text_surface, (CENTER_X-50,CENTER_Y))
        update_physics(bodies)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
