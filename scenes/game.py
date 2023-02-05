import time

import pygame
from pygame.sprite import Sprite

import random
import math
import util.const as G


# Angle: East = 0, goes CLOCKWISE

# above/under
underground = True

# TODO, make a new group
class Text:
    def __init__(self, x, y, content, timeleft, screen):
        self.x = x
        self.y = y
        self.content = content
        self.screen = screen
        self.timeleft = timeleft

    def draw(self, colour, font_size):
        render = pygame.font.SysFont(None, font_size).render(self.content, True, colour)
        self.screen.blit(render, (self.x, self.y))
        self.timeleft -= 1


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
    def __init__(self, x, y, thickness, angle, maxlength, speed, depth, colour, screen):
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

        self.colour = colour

        self.coords = [RootCoord(x, y)]
        self.subroots = []  # list of roots

        self.choppedroot = []
        self.choppedsubroots = []
        self.timesincechop = 0

    # param: Color
    def draw(self, thickness_scale=1):
        if len(self.coords) > 0:
            delta_thickness = (1 - self.thickness_scale) * self.thickness / len(self.coords)

            for i in range(len(self.coords)):
                pygame.draw.circle(self.screen, self.colour, self.coords[i].get(),
                                   round((self.thickness - i * delta_thickness) * thickness_scale / 2))
                if thickness_scale < 1:
                    self.coords[i].set(self.coords[i].x + 2 - random.random() * 4,
                                       self.coords[i].y + 2 - random.random() * 4)

            for i in range(len(self.subroots)):
                self.subroots[i].draw(thickness_scale)

        if self.timesincechop > 0:
            # print("FADING", self.timesincechop,round(255 - 10 * self.timesincechop))
            if self.timesincechop > 60:
                self.timesincechop = 0
                self.choppedroot = []
                self.choppedsubroots = []
            elif len(self.choppedroot) > 0:
                delta_thickness = (1 - self.thickness_scale) * self.thickness / len(self.choppedroot)

                # smh they cant draw transparent
                scale = 0.98 ** self.timesincechop
                for i in range(len(self.choppedroot)):
                    pygame.draw.circle(self.screen, self.colour, self.choppedroot[i].get(),
                                       round((self.thickness - i * delta_thickness) * scale / 2))
                    self.choppedroot[i].set(self.choppedroot[i].x + 2 - random.random() * 4,
                                            self.choppedroot[i].y + 2 - random.random() * 4)

                for i in range(len(self.choppedsubroots)):
                    self.choppedsubroots[i].draw(scale)

                self.timesincechop += 1

    def draw_blink(self, i):
        if len(self.coords) > 0:
            delta_thickness = (1 - self.thickness_scale) * self.thickness / len(self.coords)

            index = round(i * (len(self.coords) - 1) / G.root_counter_max)

            if index != G.root_counter_max and index != len(self.coords) - 1:
                pygame.draw.circle(self.screen, self.colour, self.coords[index].get(),
                                   round((self.thickness - index * delta_thickness) / 2) + 1)

            for j in range(len(self.subroots)):
                self.subroots[j].draw_blink(i)

    def extend(self):
        # TODO: take care of the branching out
        #   add to subroots, kill this root
        if len(self.coords) <= 0:
            return

        prev = self.coords[-1]

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
                                        self.colour,
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
                                        self.colour,
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
                if random.random() < G.extend_chance:
                    self.subroots[i].extend()

    # Returns, if wood is obtained
    # Wood is only obtained when the root chopped has subroots
    def trim(self, x, y):
        for i in range(len(self.coords)):
            if (x - self.coords[i].x) ** 2 + (y - self.coords[i].y) ** 2 < G.collision_thres:
                print("CHOPPING")
                got_wood = len(self.choppedsubroots) <= 0 < len(self.subroots)

                self.choppedroot.extend(self.coords[i:])
                self.coords = self.coords[:i]
                if len(self.coords) > 0:
                    self.alive = True  # Remove this if the branch needs to stay dead
                self.choppedsubroots.extend(self.subroots)
                self.subroots = []
                self.timesincechop = 1
                return got_wood
        else:
            got_wood = False
            for i in range(len(self.subroots)):
                if self.subroots[i].trim(x, y):
                    got_wood = True
            return got_wood

    # Returns the depth if x,y are within a root
    def contains(self, x, y):
        for i in range(len(self.coords)):
            if (x - self.coords[i].x) ** 2 + (y - self.coords[i].y) ** 2 < G.collision_thres:
                return self.depth
        else:
            contains = 0
            for i in range(len(self.subroots)):
                cur = self.subroots[i].contains(x, y)
                if cur > 0:
                    contains = cur
            return contains


class Tree(Sprite):
    def __init__(self, x, y, num_roots, colour, screen):
        Sprite.__init__(self)
        self.size = 75
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("./assets/tree-trunk.png"), (self.size, self.size)), random.randint(0, 359))

        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.screen = screen
        self.colour = colour

        self.boundaries = [
            self.x - self.size / 3,
            self.y - self.size / 3,
            self.x + self.size / 3,
            self.y + self.size / 3
        ]

        self.roots = self.init_roots(num_roots)  # List of roots

    def init_roots(self, num):
        init_angle = random.randint(0, 360)
        delta_angle = 360 // num
        angle_error = 180 // num
        root_list = []
        for i in range(num):
            newroot = Root(self.x, self.y, G.root_thickness, init_angle, G.root_maxlength, G.root_speed, 1, self.colour, self.screen)
            init_angle = (init_angle + random.randint(delta_angle - angle_error, delta_angle + angle_error)) % 360
            root_list.append(newroot)
        # todo: add groups? maybe
        return root_list

    def draw(self, blink_counter):
        if not underground:
            pass
        for i in range(len(self.roots)):
            self.roots[i].draw()

        for i in range(len(self.roots)):
            self.roots[i].draw_blink(blink_counter)

        self.screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))

    def trim(self, x, y):
        wood = 0
        for i in range(len(self.roots)):
            if self.roots[i].trim(x, y):
                wood += 1

        if wood > 0:
            if random.random() < G.wood_double_chance:
                wood = 2
            if random.random() < G.wood_lost_chance:
                wood = 0

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


class Rock(Sprite):
    def __init__(self, x, y, size, screen):
        Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("./assets/rock1.png"), (size, size))

        self.x = x
        self.y = y

        self.boundaries = [
            self.x + size / G.hitbox_scale,
            self.y + size / G.hitbox_scale,
            self.x + size * 3 / G.hitbox_scale,
            self.y + size * 3 / G.hitbox_scale
        ]

        self.screen = screen

    def draw(self, counter):
        if not underground:
            pass
        self.screen.blit(self.image, (self.x, self.y))

class Exit(Sprite):
    def __init__(self, x, y, screen):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load()
        self.size = 75
        self.screen = screen

        self.boundaries = [
            self.x + self.size / G.hitbox_scale,
            self.y + self.size / G.hitbox_scale,
            self.x + self.size * 3 / G.hitbox_scale,
            self.y + self.size * 3 / G.hitbox_scale
        ]

    def draw(self, counter):
        self.screen.blit(self.image, (self.x, self.y))

class Base(Sprite):
    def __init__(self, x, y, screen):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load()
        self.size = 75
        self.screen = screen

        self.boundaries = [
            self.x + self.size / G.hitbox_scale,
            self.y + self.size / G.hitbox_scale,
            self.x + self.size * 3 / G.hitbox_scale,
            self.y + self.size * 3 / G.hitbox_scale
        ]

    def draw(self, counter):
        if not underground:
            pass
        self.screen.blit(self.image, (self.x, self.y))




class Player(pygame.sprite.DirtySprite):
    def __init__(self, x, y, screen):
        pygame.sprite.DirtySprite.__init__(self)

        self.x = x
        self.y = y
        self.screen = screen
        self.direction = 0
        self.offset = 0

        # hunger
        self.max_energy = 250.0
        self.energy = 250.0

        # for moving and chewing, once this hits 0 starts consuming energy instead
        self.max_stamina = 500.0
        self.stamina = 500.0

        self.image = pygame.image.load("./assets/rat3.png")
        self.rect = pygame.Rect(x - self.image.get_width() // 2, y - self.image.get_height() // 2,
                                self.image.get_width(), self.image.get_height())

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
            target = round(math.degrees(math.atan((my - self.y) / (mx - self.x))))
            if mx < self.x:
                target += 180

        delta_angle = (self.direction - target) % 360

        # delta_angle)
        self.direction = target

        self.draw()

    def near_mouse(self):
        mx, my = pygame.mouse.get_pos()
        return (self.x - mx) ** 2 + (self.y - my) ** 2 <= (self.image.get_width() // 2 + 10) ** 2

    def move(self, speed):
        delta_x = math.cos(math.radians(self.direction)) * speed
        delta_y = math.sin(math.radians(self.direction)) * speed

        mx, my = pygame.mouse.get_pos()

        if not self.near_mouse() and self.stamina > 0:
            self.trail.insert(0, (self.x, self.y))
            if len(self.trail) > self.traillength:
                self.trail.pop()

            self.x += delta_x
            self.y += delta_y

            self.stamina -= G.moving_stamina_cost
        else:
            self.stamina = min(self.max_stamina, self.stamina + G.idle_stamina_regen)

        self.draw()

    def draw(self):
        for i in range(len(self.trail)):
            pygame.draw.circle(self.screen, G.trail_colour, self.trail[i], self.image.get_width() // (i + 3))

        rotated = pygame.transform.rotate(self.image, -self.direction - self.offset)
        self.screen.blit(rotated,
                         (self.x - rotated.get_width() // 2,
                          self.y - rotated.get_height() // 2))  # (self.x-self.image.get_width()//2, self.y-self.image.get_height()//2))

    def get_mouth(self):
        radius = self.image.get_width() // 2
        x = self.x + radius * math.cos(math.radians(self.direction))
        y = self.y + radius * math.sin(math.radians(self.direction))

        return x, y


class Game:
    def __init__(self, screen):
        self.trees = []


def near_exit(exits, rat):
    for i in exits:
        b = i.boundaries
        if b[0] <= rat.x <= b[2] and b[1] <= rat.y <= b[3]:
            return True

def near_base(base, rat):
    b = base.boundaries
    return b[0] <= rat.x <= b[2] and b[1] <= rat.y <= b[3]

# Entry point
def run(screen, params):
    clock = pygame.time.Clock()

    num_trees = 2
    tree_x_values = [random.randint(300, 1200) for _ in range(num_trees)]
    tree_y_values = [random.randint(100, 800) for _ in range(num_trees)]
    num_roots = [random.randint(3, 5) for _ in range(num_trees)]

    trees = [Tree(tree_x_values[i], tree_y_values[i], num_roots[i], random.choice(G.root_colours), screen) for i in range(num_trees)]

    num_rocks = 6
    rock_x_values = [random.randint(300, 1200) for _ in range(num_rocks)]
    rock_y_values = [random.randint(100, 800) for _ in range(num_rocks)]
    rock_size = [random.randint(50, 150) for _ in range(num_rocks)]

    rocks = [Rock(rock_x_values[i], rock_y_values[i], rock_size[i], screen) for i in range(num_rocks)]

    objects = trees + rocks

    rat = Player(500, 500, screen)

    update_counter = 0

    chopping_meter = 0
    chopping_location = (0, 0)
    chopping_depth = 0

    total_wood = 0

    required_power = [1, 300, 150, 75, 38, 20, 1]  # for chopping trees
    power_colour = ["black", "red", "orange", "yellow", "green", "cyan", "black"]

    display_text = []

    if underground:
        bg = pygame.Surface(G.size)
        # tiles = [pygame.image.load("./assets/dirt1.png"),
        #          pygame.image.load("./assets/dirt2.png"),
        #          pygame.image.load("./assets/dirt3.png"),
        #          pygame.image.load("./assets/dirt-simple.png")]
        #
        # for i in range(50):
        #     for j in range(30):
        #         t = pygame.transform.scale(random.choice(tiles), (30, 30))
        #         img = pygame.transform.rotate(t, round(random.randint(0, 3)) * 90)
        #         bg.blit(img, (i * 30, j * 30, 30, 30))

        for i in range(10):
            for j in range(6):
                tile = pygame.transform.rotate(pygame.image.load("./assets/dirt-simple.png"), round(random.randint(0, 3)) * 90)
                bg.blit(tile, (i * 150, j * 150, 150, 150))

    else:
        bg = pygame.Surface(G.size)
        tiles = []

        for i in range(50):
            for j in range(30):
                img = pygame.transform.rotate(random.choice(tiles), round(random.randint(0, 3)) * 90)
                bg.blit(img, (i * 30, j * 30, 30, 30))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0, {}

        if underground:
            screen.blit(bg, (0, 0, 1500, 900))

            px, py = rat.get_mouth()
            mx, my = pygame.mouse.get_pos()

            for obj in objects:
                obj.draw(update_counter)

            # the root depth if mouse is currently hovering over one

            try:
                hover_root_depth = [i.contains(mx, my) for i in trees if i.contains(mx, my)][0]
            except:
                hover_root_depth = 0
            wood_colour = "white"

            if pygame.mouse.get_pressed(3)[0] and rat.near_mouse() and hover_root_depth > 0:
                if chopping_meter == 0:
                    chopping_location = (mx, my)
                    chopping_depth = hover_root_depth
                else:
                    if (mx - chopping_location[0]) ** 2 + (my - chopping_location[1]) ** 2 > 4:
                        chopping_meter = -1

                chopping_meter += 1
                if rat.stamina <= 0:
                    chopping_meter = 0
                else:
                    rat.stamina -= G.chopping_stamina_cost_base

                    pygame.draw.line(screen, power_colour[hover_root_depth],
                                     (round(rat.x) - rat.image.get_width() // 2,
                                      round(rat.y) - rat.image.get_height()),
                                     (round(rat.x - rat.image.get_width() // 2 + rat.image.get_width() * (
                                                 chopping_meter / required_power[hover_root_depth])),
                                      round(rat.y) - rat.image.get_height()), 10)

                if chopping_meter > required_power[hover_root_depth]:
                    chopping_meter = 0
                    for i in trees:
                        wood_obtained = i.trim(chopping_location[0], chopping_location[1])
                        if wood_obtained > 0:
                            display_text.append(
                                Text(round(rat.x) - rat.image.get_width() / 4, round(rat.y) - rat.image.get_height(),
                                     f"+{wood_obtained}", 60, screen))
                        # pygame.draw.circle(screen, "red", (px,py), 10) # makes the rat looks like a clown
                        total_wood += wood_obtained
            else:
                chopping_meter = 0

            if pygame.mouse.get_pressed(3)[0] and rat.near_mouse() and near_exit(rat):
                pass

            for text in display_text:
                if text.timeleft <= 0:
                    display_text.remove(text)
                else:
                    img = pygame.transform.scale(pygame.image.load("./assets/wood_1fab5.png"), (50, 50))
                    screen.blit(img, (text.x - rat.image.get_width() / 4, text.y - rat.image.get_height() / 4))
                    text.draw("white", 30)
                    wood_colour = "green"

            # wood counter
            wood = Text(35, 50, f"Wood: {total_wood}", 99, screen)
            wood.draw(wood_colour, 30)
            if wood_colour == "green":
                wood_colour = "white"

            # energy
            energy = Text(35, 100, f"Energy: {round(rat.energy)}", 99, screen)
            color = ["red", "yellow", "green"][max(0, round(rat.energy * 3 / rat.max_energy) - 1)]
            energy.draw(color, 30)

            # stamina bar
            color = ["red", "yellow", "green"][max(0, round(rat.stamina * 3 / rat.max_stamina) - 1)]
            pygame.draw.rect(screen, "black", pygame.Rect(34, 139, round((rat.max_stamina - 1) / 2) + 2, 32), 1)
            pygame.draw.rect(screen, color, pygame.Rect(35, 140, round(max(0, round(rat.stamina - 1)) / 2), 30))

            # stamina text
            stam = Text(115, 145, f"Stamina", 99, screen)
            stam.draw("black", 30)

            if hover_root_depth > 0:
                pygame.draw.circle(screen, power_colour[hover_root_depth], (mx, my), 10)  # makes the rat looks like a clown

            if update_counter >= G.root_counter_max:
                for i in trees:
                    i.extend()
                update_counter = 0

            rat.turn(pygame.mouse.get_pos())

            for i in objects:
                b = i.boundaries
                if b[0] <= px <= b[2] and b[1] <= py <= b[3]:
                    rat.stamina = min(rat.max_stamina, rat.stamina + G.idle_stamina_regen)
                    break
            else:
                for i in trees:
                    if i.contains(px, py):
                        rat.move(0.025)
                    else:
                        rat.move(1)

            rat.energy -= G.energy_lost

            pygame.display.flip()
            clock.tick(60)
            update_counter += 1
