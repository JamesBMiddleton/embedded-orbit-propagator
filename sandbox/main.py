# CODE ADAPTED FROM https://pythonprogramming.net/many-blob-objects-intermediate-python-tutorial/

import pygame
import random

STARTING_BLUE_BLOBS = 10
STARTING_RED_BLOBS = 3

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Propagation")
clock = pygame.time.Clock()

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Body:

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.next_pos = pos
        self.next_vel = vel
        self.size = random.randrange(4,8)

    def move(self):
        self.pos = self.next_pos
        self.vel = self.next_vel

        self.next_pos.x += self.vel.x
        self.next_pos.y += self.vel.y

        # self.next_vel.x =
        # self.next_vel.y =

        if self.pos.x < 0: self.pos.x = 0
        elif self.pos.x > WIDTH: self.pos.x = WIDTH
        
        if self.pos.y < 0: self.pos.y = 0
        elif self.pos.y > HEIGHT: self.pos.y = HEIGHT


def draw_environment(blob_list):
    game_display.fill(WHITE)

    for blob_dict in blob_list:
        for blob_id in blob_dict:
            blob = blob_dict[blob_id]
            pygame.draw.circle(game_display, (0,0,0), [blob.pos.x, blob.pos.y], blob.size)
            blob.move()

    pygame.display.update()
    

def main():
    bodies = {}
    for i in range(10):
        pos = Vector(random.randrange(0,WIDTH), random.randrange(0,HEIGHT))
        vel = Vector(random.randrange(-3,3), random.randrange(-3,3))
        bodies[i] = Body(pos, vel)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        draw_environment([bodies])
        clock.tick(120)

if __name__ == '__main__':
    main()
