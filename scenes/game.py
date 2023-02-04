import pygame
from pygame.sprite import Sprite

import random
import math
import util.const as G


class Root:
    def __init__(self, x, y, thickness, angle, maxlength, speed, depth, screen):
        self.x = x
        self.y = y
        self.speed = speed
        self.thickness = thickness
        self.thickness_scale = 0.7
        self.screen = screen
        # Maybe add a minimum thickness
        self.angle = angle
        self.alive = True
        self.maxlength = maxlength
        self.length = random.randint(maxlength//2, maxlength)
        self.depth = depth
        self.maxdepth = 4


        self.coords = [(x,y)]
        self.subroots = [] # list of roots

    def draw(self, colour):
        delta_thickness = (1 - self.thickness_scale) * self.thickness / len(self.coords)

        for i in range(len(self.coords)):
            pygame.draw.circle(self.screen, colour, list(map(round,self.coords[i])),
                             round((self.thickness - i * delta_thickness)/2))


        for i in range(len(self.subroots)):
            self.subroots[i].draw(colour)


    def extend(self):
        # TODO: take care of the branching out
        #   add to subroots, kill this root
        prev_x, prev_y = self.coords[-1]

        if len(self.coords) >= self.length and self.alive and self.depth <= self.maxdepth:
            print("Branching out")
            self.alive = False

            pdt = [0.05, 0.1, 0.8, 1]

            new_branches = random.random()
            for i in range(len(pdt)):
                if new_branches <= pdt[i]:
                    print("NEW", new_branches, i)

                    # Angle
                    if i == 1:
                        new_root = Root(prev_x, prev_y,
                                        max(self.thickness * self.thickness_scale, 5),
                                        self.angle + random.randint(-10, 10),
                                        self.maxlength * 2,
                                        max(self.speed * 0.7, 1),
                                        self.depth + 1,
                                        self.screen)

                        self.subroots.append(new_root)
                        break

                    init_angle = random.randint(30, 50)
                    for j in range(i):
                        new_root = Root(prev_x, prev_y,
                                        max(self.thickness * self.thickness_scale, 5),
                                        self.angle + init_angle,
                                        self.maxlength * 2,
                                        max(self.speed * 0.7, 1),
                                        self.depth + 1,
                                        self.screen)
                        init_angle -= random.randint(20, 60)
                        self.subroots.append(new_root)
                    break

        if self.alive:
            delta_x = math.cos(math.radians(self.angle))*self.speed
            delta_y = math.sin(math.radians(self.angle))*self.speed

            self.angle += 5 - random.random() * 10
            self.coords.append((prev_x+delta_x, prev_y+delta_y))

        else:
            for i in range(len(self.subroots)):
                self.subroots[i].extend()

    def collide(self, x, y):
        pass # modify the tree (trims the extra branches)

    def trim(self, x, y):
        pass


class Tree(Sprite):
    def __init__(self, x, y, screen):
        Sprite.__init__(self)

        # TODO insert image
        # self.image = pygame.Surface()

        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.screen = screen

        self.roots = [] # List of roots

        # TODO: initialize roots


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # TODO




class Game:
    def __init__(self, screen):
        self.trees = []


# Entry point
def run(screen, params):
    clock = pygame.time.Clock()

    tree = Root(500, 500, 20, 0, 20, 5, 1, screen)

    root_update_counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0, {}

        screen.fill(G.bg_colour)
        if root_update_counter < 30:
            tree.draw(G.root_colour)
        else:
            tree.draw(G.root_colour2)

        if root_update_counter > 30:
            tree.extend()
            root_update_counter = 0

        pygame.display.flip()
        clock.tick(60)
        root_update_counter += 1