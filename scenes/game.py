import time

import pygame
from pygame.sprite import Sprite

import random
import math
import util.const as G


# Angle: East = 0, goes CLOCKWISE


# TODO, make a new group
class RootCoord(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.x = x
        self.y = y

    def get(self):
        return (round(self.x), round(self.y))

    def set(self, x, y):
        self.x = x
        self.y = y


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
        self.length = random.randint(maxlength // 2, maxlength)
        self.depth = depth
        self.maxdepth = 4

        self.coords = [RootCoord(x, y)]
        self.subroots = []  # list of roots

        self.choppedroot = []
        self.choppedsubroots = []
        self.timesincechop = 0

    # param: Color
    def draw(self, colour, thickness_scale=1):
        if len(self.coords) > 0:
            delta_thickness = (1 - self.thickness_scale) * self.thickness / len(self.coords)

            for i in range(len(self.coords)):
                pygame.draw.circle(self.screen, colour, self.coords[i].get(),
                                   round((self.thickness - i * delta_thickness) * thickness_scale / 2))
                if thickness_scale < 1:
                    self.coords[i].set(self.coords[i].x + 2 - random.random() * 4, self.coords[i].y + 2 - random.random() * 4)

            for i in range(len(self.subroots)):
                self.subroots[i].draw(colour, thickness_scale)

        if self.timesincechop > 0:
            # print("FADING", self.timesincechop,round(255 - 10 * self.timesincechop))
            if self.timesincechop > 60:
                self.timesincechop = 0
                self.choppedroot = []
                self.choppedsubroots = []
            elif len(self.choppedroot) > 0:
                delta_thickness = (1 - self.thickness_scale) * self.thickness / len(self.choppedroot)

                # smh they cant draw transparent
                scale = 0.98**self.timesincechop
                for i in range(len(self.choppedroot)):
                    pygame.draw.circle(self.screen, colour, self.choppedroot[i].get(),
                                       round((self.thickness - i * delta_thickness) * scale / 2))
                    self.choppedroot[i].set(self.choppedroot[i].x + 2 - random.random() * 4, self.choppedroot[i].y + 2 - random.random() * 4)

                for i in range(len(self.choppedsubroots)):
                    self.choppedsubroots[i].draw(colour, scale)

                self.timesincechop += 1

    def draw_blink(self, i):
        if len(self.coords) > 0:
            delta_thickness = (1 - self.thickness_scale) * self.thickness / len(self.coords)

            index = round(i * (len(self.coords) - 1) / G.root_counter_max)

            if index != G.root_counter_max and index != len(self.coords) - 1:
                pygame.draw.circle(self.screen, G.root_colour, self.coords[index].get(),
                               round((self.thickness - index * delta_thickness) / 2) + 1)

            for j in range(len(self.subroots)):
                self.subroots[j].draw_blink(i)

    def extend(self):
        # TODO: take care of the branching out
        #   add to subroots, kill this root
        if len(self.coords) <= 0:
            return

        prev = self.coords[-1]

        # if self.x <= 0 or self.x >= 600 or self.y <= 0 or self.y >= 600:
        #     return

        if len(self.coords) >= self.length and self.alive and self.depth <= self.maxdepth:
            print("Branching out")
            self.alive = False

            pdt = [0.02, 0.1, 0.8, 1]

            new_branches = random.random()
            for i in range(len(pdt)):
                if new_branches <= pdt[i]:
                    print("NEW", new_branches, i)

                    # Angle
                    if i == 1:
                        new_root = Root(prev.x, prev.y,
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
                        new_root = Root(prev.x, prev.y,
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
            delta_x = math.cos(math.radians(self.angle)) * self.speed
            delta_y = math.sin(math.radians(self.angle)) * self.speed

            self.angle += 5 - random.random() * 10
            self.coords.append(RootCoord(prev.x + delta_x, prev.y + delta_y))
            # print(prev.x, prev.y)

        else:
            for i in range(len(self.subroots)):
                self.subroots[i].extend()

    # Returns, if wood is obtained
    # Wood is only obtained when the root chopped has subroots
    def trim(self, x, y):
        for i in range(len(self.coords)):
            if (x-self.coords[i].x) ** 2 + (y-self.coords[i].y) ** 2 < G.collision_thres:
                print("CHOPPING")
                got_wood = len(self.choppedsubroots) <= 0 and len(self.subroots) > 0

                self.choppedroot.extend(self.coords[i:])
                self.coords = self.coords[:i]
                self.choppedsubroots.extend(self.subroots)
                self.subroots = []
                self.timesincechop = 1
                return got_wood
        else:
            got_wood = False
            for i in range(len(self.subroots)):
                if self.subroots[i].trim(x,y):
                    got_wood = True
            return got_wood
        
    # Returns the depth if x,y are within a root
    def contains(self, x, y):
        for i in range(len(self.coords)):
            if (x-self.coords[i].x) ** 2 + (y-self.coords[i].y) ** 2 < G.collision_thres:
                return self.depth
        else:
            contains = 0
            for i in range(len(self.subroots)):
                cur = self.subroots[i].contains(x,y)
                if cur > 0:
                    contains = cur
            return contains


class Tree(Sprite):
    def __init__(self, x, y, num_roots, screen):
        Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("./assets/tree-trunk.png"), (75, 75))

        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.screen = screen
        self.colour = pygame.Color(G.root_colour)

        self.roots = self.init_roots(num_roots)  # List of roots

    def init_roots(self, num):
        init_angle = random.randint(0, 360)
        delta_angle = 360//num
        angle_error = 15
        root_list = []
        for i in range(num):
            newroot = Root(self.x, self.y, G.root_thickness, init_angle, G.root_maxlength, G.root_speed, 1, self.screen)
            init_angle = (init_angle + random.randint(delta_angle-angle_error, delta_angle+angle_error)) % 360
            root_list.append(newroot)
        # todo: add groups? maybe
        return root_list

    def draw(self, blink_counter):
        for i in range(len(self.roots)):
            self.roots[i].draw(self.colour)

        for i in range(len(self.roots)):
            self.roots[i].draw_blink(blink_counter)

        self.screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))

    def trim(self, x, y):
        wood = 0
        for i in range(len(self.roots)):
            if self.roots[i].trim(x, y):
                wood += 1

        return wood

    def extend(self):
        for i in range(len(self.roots)):
            self.roots[i].extend()

    def contains(self, x, y):
        contains = 0
        for i in range(len(self.roots)):
            cur = self.roots[i].contains(x, y)
            if cur > 0:
                contains = cur
        return contains
        

class Player(pygame.sprite.DirtySprite):
    def __init__(self, x, y, screen):
        pygame.sprite.DirtySprite.__init__(self)

        self.x = x
        self.y = y
        self.speed = 2
        self.screen = screen
        self.direction = 0
        self.offset = 0

        self.image = pygame.image.load("./assets/rat2.png")
        self.rect = pygame.Rect(x-self.image.get_width()//2, y-self.image.get_height()//2, self.image.get_width(), self.image.get_height())

        self.trail = []
        self.traillength = 30

    def turn(self, mouse):
        mx, my = mouse

        target = 270
        if mx == self.x:
            if my > self.y:
                target = -90
            else:
                target = 90
        else:
            target = round(math.degrees(math.atan((my-self.y)/(mx-self.x))))
            if mx<self.x:
                target += 180

        delta_angle = (self.direction - target) % 360

        # delta_angle)
        self.direction = target

        self.draw()

    def near_mouse(self):
        mx, my = pygame.mouse.get_pos()
        return (self.x-mx)**2 + (self.y-my)**2 <= (self.image.get_width()//2 + 5)**2

    def move(self):
        delta_x = math.cos(math.radians(self.direction)) * self.speed
        delta_y = math.sin(math.radians(self.direction)) * self.speed

        mx, my = pygame.mouse.get_pos()

        if not self.near_mouse():
            self.trail.insert(0, (self.x, self.y))
            if len(self.trail) > self.traillength:
                self.trail.pop()

            self.x += delta_x
            self.y += delta_y

        self.draw()

    def draw(self):
        for i in range(len(self.trail)):
            pygame.draw.circle(self.screen, G.trail_colour, self.trail[i], self.image.get_width()//(i+3))

        rotated = pygame.transform.rotate(self.image, -self.direction - self.offset)
        self.screen.blit(rotated,
                         (self.x-rotated.get_width()//2, self.y - rotated.get_height()//2)) # (self.x-self.image.get_width()//2, self.y-self.image.get_height()//2))

    def get_mouth(self):
        radius = self.image.get_width()//2
        x = self.x + radius * math.cos(math.radians(self.direction))
        y = self.y + radius * math.sin(math.radians(self.direction))

        return x,y


class Game:
    def __init__(self, screen):
        self.trees = []


# Entry point
def run(screen, params):
    clock = pygame.time.Clock()

    tree = Tree(700, 500, 4, screen)
    # tree = Root(700, 500, 20, 0, 20, 5, 1, screen)
    # tree2 = Root(700, 500, 20, 120, 20, 5, 1, screen)
    # tree3 = Root(700, 500, 20, 240, 20, 5, 1, screen)

    rat = Player(500, 500, screen)

    root_update_counter = 0

    chopping_meter = 0
    chopping_location = (0,0)
    chopping_depth = 0
    
    required_power = [0, 300, 120, 60, 20, 0, 0] # for chopping trees
    power_colour = ["black", "red", "orange", "yellow", "green", "black", "black"]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0, {}

        screen.fill(G.bg_colour)

        px, py = rat.get_mouth()
        mx, my = pygame.mouse.get_pos()

        tree.draw(root_update_counter)

        # the root depth if mouse is currently hovering over one
        hover_root_depth = tree.contains(mx, my)

        if pygame.mouse.get_pressed(3)[0] and rat.near_mouse() and hover_root_depth > 0:
            if chopping_meter == 0:
                chopping_location = (mx, my)
                chopping_depth = hover_root_depth
            else:
                if (mx-chopping_location[0]) ** 2 + (my - chopping_location[1]) ** 2 > 4:
                    chopping_meter = -1

            chopping_meter += 1
            pygame.draw.line(screen, power_colour[hover_root_depth] , (round(rat.x) - rat.image.get_width()//2, round(rat.y)- rat.image.get_height()),
                             (round(rat.x - rat.image.get_width()//2 + rat.image.get_width() * (chopping_meter/required_power[hover_root_depth])), 
                              round(rat.y)- rat.image.get_height()), 10) 

            if chopping_meter > required_power[hover_root_depth]:
                chopping_meter = 0
                woods_obtained = tree.trim(chopping_location[0], chopping_location[1])
                if woods_obtained > 0:
                    print("WOODS OBTAINED:", woods_obtained)
                # pygame.draw.circle(screen, "red", (px,py), 10) # makes the rat looks like a clown
        else:
            chopping_meter = 0

        if hover_root_depth > 0:
            pygame.draw.circle(screen, "red", (mx, my), 10)  # makes the rat looks like a clown

        if root_update_counter >= G.root_counter_max:
            tree.extend()
            root_update_counter = 0

        rat.turn(pygame.mouse.get_pos())
        rat.move()

        pygame.display.flip()
        clock.tick(60)
        root_update_counter += 1
