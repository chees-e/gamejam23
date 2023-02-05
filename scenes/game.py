import time

import pygame
from pygame.sprite import Sprite

import random
import math
import util.const as G

# Groups (global var for now)
group_root = pygame.sprite.Group()
group_underground = pygame.sprite.Group()
group_aboveground = pygame.sprite.Group()
group_all = pygame.sprite.Group()
group_u_obstacles = pygame.sprite.Group()
group_a_obstacles = pygame.sprite.Group()
group_u_mats = pygame.sprite.Group()
group_a_mats = pygame.sprite.Group()

# Angle: East = 0, goes CLOCKWISE
def get_theta(x1, y1, x2, y2):  # Starts east, clockwise rotation
    if x2 == x1:
        if y2 > y1:
            target = -90
        else:
            target = 90
    else:
        target = round(math.degrees(math.atan((y2 - y1) / (x2 - x1))))
        if x2 < x1:
            target += 180
    return target


# above/under
underground = True
screen_offset = 0  # in the x direction


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
    def __init__(self, x, y, depth):
        Sprite.__init__(self)
        self.x = x
        self.y = y

        minthickness = G.root_thickness // (2 ** depth)
        self.rect = pygame.Rect(self.x - screen_offset - minthickness // 2, self.y - minthickness // 2, minthickness,
                                minthickness)
        self.depth = depth
        group_root.add(self)

    def get(self):
        return (round(self.x - screen_offset), round(self.y))

    def set(self, x, y):  # TODO check
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x - screen_offset


class Material(Sprite):
    def __init__(self, x, y, value, under=True):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = 50
        self.under = under
        self.value = value # 0, 1, 2
        if not under:
            self.image = random.choice(
                [pygame.transform.scale(pygame.image.load("./assets/apple.png"), (self.size, self.size)),
                pygame.transform.scale(pygame.image.load("./assets/carrot.png"), (self.size, self.size)),
                pygame.transform.scale(pygame.image.load("./assets/cheese.png"), (self.size, self.size))]
            )
        else:
            self.image = pygame.transform.scale(pygame.image.load("./assets/iron.png"), (self.size, self.size))

        self.rect = pygame.Rect(self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2,
                                self.image.get_width(), self.image.get_height())

    def update(self):
        self.rect.x = self.x - screen_offset

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

        self.coords = [RootCoord(x, y, depth)]
        self.subroots = []  # list of roots

        self.choppedroot = []
        self.choppedsubroots = []
        self.timesincechop = 0

    # param: Color
    def draw(self, thickness_scale=1):
        if not underground:
            return
        if len(self.coords) > 0:
            delta_thickness = (1 - self.thickness_scale) * self.thickness / len(self.coords)

            for i in range(len(self.coords)):
                pygame.draw.circle(self.screen, self.colour, self.coords[i].get(),
                                   round((self.thickness - i * delta_thickness) * thickness_scale / 2))
                if thickness_scale < 1:
                    group_root.remove(self.coords[i])
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
                    group_root.remove(self.choppedroot[i])
                    pygame.draw.circle(self.screen, self.colour, self.choppedroot[i].get(),
                                       round((self.thickness - i * delta_thickness) * scale / 2))
                    self.choppedroot[i].set(self.choppedroot[i].x + 2 - random.random() * 4,
                                            self.choppedroot[i].y + 2 - random.random() * 4)

                for i in range(len(self.choppedsubroots)):
                    self.choppedsubroots[i].draw(scale)

                self.timesincechop += 1

    def draw_blink(self, i):
        if not underground:
            return
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
            # print("Branching out")
            self.alive = False

            pdt = {
                1: [0.02, 0.1, 0.8, 1],
                2: [0.05, 0.15, 0.8, 1],
                3: [0.1, 0.3, 0.9, 1],
                4: [0.4, 0.6, 0.95, 1],
                5: [0.5, 0.7, 0.99, 1],
            }
            new_branches = random.random()
            for i in range(len(pdt[1])):
                if new_branches <= pdt[self.depth][i]:
                    # print("NEW", new_branches, i)

                    # Angle
                    if i == 1:
                        new_root = Root(prev.x, prev.y,
                                        max(self.thickness * self.thickness_scale, 5),
                                        self.angle + random.randint(-10, 10),
                                        self.maxlength * 2,
                                        max(self.speed * 0.8, 1),
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
                                        max(self.speed * 0.8, 1),
                                        self.depth + 1,
                                        self.colour,
                                        self.screen)
                        init_angle -= random.randint(20, 60)
                        self.subroots.append(new_root)
                    break

        random_factor = 2 / (self.depth)

        if self.alive and random.random() < random_factor:
            delta_x = math.cos(math.radians(self.angle)) * self.speed
            delta_y = math.sin(math.radians(self.angle)) * self.speed

            self.coords.append(RootCoord(prev.x + delta_x, prev.y + delta_y, self.depth))

            collided_block = pygame.sprite.spritecollideany(self.coords[-1], group_underground)

            if collided_block is not None:
                print("Collided")
                rockx, rocky = collided_block.rect.center
                rock_dir = get_theta(prev.x + delta_x, prev.y + delta_y, rockx, rocky)
                delta_angle = self.angle - rock_dir
                if delta_angle == 0:
                    self.angle += 10
                else:
                    self.angle += 45 / delta_angle
                self.coords.pop()
            else:
                self.angle += 5 - random.random() * 10

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


class Tree(Sprite):
    def __init__(self, x, y, num_roots, colour, screen):
        Sprite.__init__(self)
        self.size = 75
        self.image = pygame.transform.scale(pygame.image.load("./assets/tree-trunk.png"), (self.size, self.size))

        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2,
                                self.image.get_width(), self.image.get_height())
        self.radius = self.size / G.hitbox_scale

        self.underground_y_offset = 10

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
            newroot = Root(self.x, self.y, G.root_thickness, init_angle, G.root_maxlength, G.root_speed, 1, self.colour,
                           self.screen)
            init_angle = (init_angle + random.randint(delta_angle - angle_error, delta_angle + angle_error)) % 360
            root_list.append(newroot)
        return root_list

    def draw(self):
        y = self.y - self.image.get_height() // 2

        if not underground:
            self.image = pygame.image.load("./assets/tree.png")
            y -= 100 - self.underground_y_offset

        else:
            self.image = pygame.transform.scale(pygame.image.load("./assets/tree-trunk.png"), (self.size, self.size))

        self.screen.blit(self.image, (self.x - self.image.get_width() // 2 - screen_offset, y))
        self.rect = pygame.Rect(self.x - self.image.get_width() // 2 - screen_offset,
                                self.y - self.image.get_height() // 2, self.image.get_width(), self.image.get_height())

    def drawroots(self, blink_counter):
        if underground:
            for i in range(len(self.roots)):
                self.roots[i].draw()

            for i in range(len(self.roots)):
                self.roots[i].draw_blink(blink_counter)

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

    def update(self):
        self.rect.x = self.x - self.image.get_width() // 2 - screen_offset
        if underground:
            self.rect.y = self.y - self.image.get_height() // 2
        else:
            self.rect.y = self.y - self.image.get_height() // 2 - self.underground_y_offset


class Rock(Sprite):
    def __init__(self, x, y, screen):
        Sprite.__init__(self)
        self.size = random.randint(50, 100)
        self.image = pygame.transform.scale(pygame.image.load("./assets/rock-underground.png"), (self.size, self.size))
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.image.get_width() // 2, self.y - self.image.get_width() // 2,
                                self.image.get_width(), self.image.get_height())
        self.radius = self.size / G.hitbox_scale
        self.under = True

        self.boundaries = [
            self.x + self.size / G.hitbox_scale,
            self.y + self.size / G.hitbox_scale,
            self.x + self.size * 3 / G.hitbox_scale,
            self.y + self.size * 3 / G.hitbox_scale
        ]

        self.screen = screen

    def update_image(self, under):
        if self.under != under:
            if under:
                self.image = pygame.transform.scale(pygame.image.load("./assets/rock-underground.png"),
                                                    (self.size, self.size))
            else:
                self.image = pygame.transform.scale(pygame.image.load("./assets/rock1.png"), (self.size, self.size))

    def update(self):
        self.rect.x = self.x - self.image.get_width() // 2 - screen_offset

    # def draw(self, counter):
    #     if not underground: # make this a function to switch
    #         self.image = pygame.transform.scale(pygame.image.load("./assets/rock1.png"), (self.size, self.size))
    #     self.screen.blit(self.image, (self.x, self.y))

class Bush(Sprite):
    def __init__(self, x, y, screen):
        Sprite.__init__(self)
        self.size = random.randint(25, 50)
        self.image = pygame.transform.scale(pygame.image.load("./assets/bush.png"), (self.size, self.size))
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.image.get_width() // 2, self.y - self.image.get_width() // 2,
                                self.image.get_width(), self.image.get_height())
        self.radius = self.size / G.hitbox_scale
        self.under = True

        self.boundaries = [
            self.x + self.size / G.hitbox_scale,
            self.y + self.size / G.hitbox_scale,
            self.x + self.size * 3 / G.hitbox_scale,
            self.y + self.size * 3 / G.hitbox_scale
        ]

        self.screen = screen

    def update(self):
        self.rect.x = self.x - self.image.get_width() // 2 - screen_offset


class Exit(Sprite):
    def __init__(self, x, y, screen):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = 75
        self.image = pygame.transform.scale(pygame.image.load("./assets/exit.png"), (self.size, self.size))
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.screen = screen

        self.boundaries = [999, 999, -999, -999]

        self.triggers = [
            self.x + self.size / G.hitbox_scale - 20,
            self.y + self.size / G.hitbox_scale - 20,
            self.x + self.size * 3 / G.hitbox_scale + 20,
            self.y + self.size * 3 / G.hitbox_scale + 20
        ]

    def update(self):
        self.rect.x = self.x - screen_offset
    # def draw(self, counter):
    #     self.screen.blit(self.image, (self.x, self.y))


class Nest(Sprite):
    def __init__(self, x, y, screen):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load("./assets/nest.png")
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.screen = screen

        self.boundaries = [999, 999, -999, -999]

        self.triggers = [  # TODO check collisions
            self.x,
            self.y,
            self.x + 150,
            self.y + 100
        ]
        print(self.triggers)

    # def draw(self, counter):
    #     self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.x = self.x - screen_offset


# Used for collision detection
class Temp(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.rect = pygame.Rect(x - 1, y - 1, 3, 3)


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
        self.stamina = 0.0

        self.image = pygame.image.load("./assets/rat3.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.radius = self.width // 2
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2,
                                self.image.get_width(), self.image.get_height())

        self.trail = []
        self.traillength = 25

        self.upgrade_level = [
            [],
            [0, 0.2],  # spd
            [0, -0.05],  # move cost
            [0, 50],  # max stam
            [0, 0.05],  # stam regen
            [0, 0.004]  # energy cost
        ]

        self.spd = 2 + self.upgrade_level[1][0] * self.upgrade_level[1][-1]
        self.move_cost = G.moving_stamina_cost + self.upgrade_level[2][0] * self.upgrade_level[2][-1]
        self.max_stamina += self.upgrade_level[3][0] * self.upgrade_level[3][-1]
        self.stamina_regen = G.idle_stamina_regen + self.upgrade_level[4][0] * self.upgrade_level[4][-1]
        self.energy_cost = G.energy_lost + self.upgrade_level[5][0] * self.upgrade_level[5][-1]

    def turn(self, mouse):
        mx, my = mouse
        target = get_theta(self.x - screen_offset, self.y, mx, my)

        self.direction = target

        self.draw()

    def near_mouse(self):
        mx, my = pygame.mouse.get_pos()
        return (self.x - screen_offset - mx) ** 2 + (self.y - my) ** 2 <= (self.image.get_width() // 2 + 10) ** 2

    def move(self, speed):
        global screen_offset, group_u_obstacles

        delta_x = math.cos(math.radians(self.direction)) * speed
        delta_y = math.sin(math.radians(self.direction)) * speed

        mx, my = pygame.mouse.get_pos()

        if not self.near_mouse() and self.stamina > 0:
            self.trail.insert(0, (self.x, self.y))
            if len(self.trail) > self.traillength:
                self.trail.pop()

            self.x += delta_x
            self.y += delta_y

            if not underground and self.x > 2*G.width-2*60-12:
                self.x -= delta_x

            self.rect.x = self.x - screen_offset - self.width // 2
            self.rect.y = self.y - self.height // 2

            # for obs in group_u_obstacles.sprites():
            #     if pygame.sprite.collide_circle(self, obs):
            #         self.x -= delta_x
            #         self.y -= delta_y
            #         self.stamina = min(self.max_stamina, self.stamina + G.idle_stamina_regen)
            #         break
            # else:
            if self.x - screen_offset < G.tiles_width:
                screen_offset = max(0, screen_offset - (G.tiles_width - (self.x - screen_offset)))
            elif self.x - screen_offset > G.width - G.tiles_width:
                screen_offset = min(G.width, self.x - (G.width - G.tiles_width))
                print(screen_offset)
            self.stamina -= G.moving_stamina_cost
        else:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen)

        self.draw()

    def draw(self):
        for i in range(len(self.trail)):
            curtrail = self.trail[i]
            pygame.draw.circle(self.screen, G.trail_colour, (curtrail[0] - screen_offset, curtrail[1]),
                               self.image.get_width() // (i + 3))
        rotated = pygame.transform.rotate(self.image, -self.direction - self.offset)
        self.screen.blit(rotated,
                         (self.x - rotated.get_width() // 2 - screen_offset,
                          self.y - rotated.get_height() // 2))  # (self.x-self.image.get_width()//2, self.y-self.image.get_height()//2))

    def get_mouth(self):
        radius = self.image.get_width() // 2
        x = self.x - screen_offset + radius * math.cos(math.radians(self.direction))
        y = self.y + radius * math.sin(math.radians(self.direction))

        return x, y


# TODO Update proximity checks
# BOunds should be absolute
def near_exit(exits, rat):
    for i in exits:
        b = i.triggers
        if b[0] <= rat.x <= b[2] and b[1] <= rat.y <= b[3]:
            return True


def near_nest(nests, rat):
    if not underground:
        return False
    for nest in nests:
        b = nest.triggers
        if b[0] <= rat.x <= b[2] and b[1] <= rat.y <= b[3]:
            return True
    else:
        return False


def in_proximity(c, acc):
    if acc:
        for i in acc:
            if (c[0] - i[0]) ** 2 + (c[1] - i[1]) ** 2 <= (G.proximity_value ** 2):
                return True
        return False
    else:
        return False


def get_map_items(num_items):
    if num_items > 2 * G.max_tiles:
        print("Too many tiles")
        return []
    acc = []
    tiles = random.sample([(i, j) for i in range(1, 2 * G.tiles_x - 1) for j in range(1, G.tiles_y - 1)], num_items)
    if tiles[0][0] > (G.tiles_y - 2):
        tiles.pop(0)
        newtile = (random.randint(1, G.tiles_x - 2), random.randint(1, G.tiles_y - 2))
        while newtile in tiles:
            newtile = (random.randint(1, G.tiles_x - 2), random.randint(1, G.tiles_y - 2))
        tiles.insert(0, newtile)  # Guarantees the first tile to be in the first frame

    print(tiles)
    for (tilex, tiley) in tiles:
        minx = tilex * G.tiles_width + G.tile_offset
        maxx = (tilex + 1) * G.tiles_width - G.tile_offset
        miny = tiley * G.tiles_height + G.tile_offset
        maxy = (tiley + 1) * G.tiles_height - G.tile_offset

        acc.append((random.randint(minx, maxx), random.randint(miny, maxy)))

    return acc


# TODO TODO: Fix collision (both levels)
## Entry point
def run(screen, params):
    global underground, screen_offset
    clock = pygame.time.Clock()

    # 0, nests, Rocks_u, rocks_a, bushes,  exits, trees
    num_items = [0, 3, 18, 8, 20, 4, 10, 0]
    num_mats = 5
    item_r = [sum(num_items[:i + 1]) for i in range(len(num_items))]  # item range
    print(item_r)
    num_roots = [random.randint(3, 5) for _ in range(num_items[4])]

    points = get_map_items(item_r[-1])  # 1 unused (nest)
    print(points)

    # generate nest
    nests = [Nest(i[0], i[1], screen) for i in points[item_r[0]:item_r[1]]]
    # nest = Nest(nest_location[0], nest_location[1], screen)
    # generate rocks first
    # underground rocks
    u_rocks = [Rock(i[0], i[1], screen) for i in points[item_r[1]:item_r[2]]]

    # aboveground rocks
    a_rocks = [Rock(i[0], i[1], screen) for i in points[item_r[2]:item_r[3]]]

    # bushes
    bushes = [Bush(i[0], i[1], screen) for i in points[item_r[3]:item_r[4]]]

    # generate exits
    exits = [Exit(i[0], i[1], screen) for i in points[item_r[4]:item_r[5]]]

    # generate trees last
    trees = [Tree(i[0], i[1], random.choice(num_roots), random.choice(G.root_colours), screen) for i in
             points[item_r[5]:item_r[6]]]

    for i in range(num_mats):
        group_a_mats.add(Material(random.randint(G.tiles_width, 2*(G.width-G.tiles_width)),
                                  random.randint(G.tiles_height, G.height-G.tiles_height), random.randint(0,2), False))
        group_u_mats.add(Material(random.randint(G.tiles_width, 2*(G.width-G.tiles_width)),
                                  random.randint(G.tiles_height, G.height-G.tiles_height), 1, True))

    # TODO try using groups
    underground_objects = u_rocks + exits + nests
    aboveground_objects = a_rocks + bushes + exits  # + trees
    group_underground.add(underground_objects)
    group_aboveground.add(aboveground_objects)

    group_all.add(underground_objects, aboveground_objects, trees, group_u_mats, group_a_mats)
    group_u_obstacles.add(trees, u_rocks)
    group_a_obstacles.add(trees, a_rocks)

    # [print(i.x, i.y) for i in underground_objects]

    rat = Player(nests[0].x + 75, nests[0].y + 75, screen)

    update_counter = 0

    chopping_meter = 0
    chopping_location = (0, 0)
    chopping_depth = 0

    total_wood = 0
    total_iron = 0

    required_power = [1, 300, 150, 75, 38, 20, 1]  # for chopping trees
    power_colour = ["black", "red", "orange", "yellow", "green", "cyan", "black"]

    display_text = []

    u_bg = pygame.Surface((2 * G.width, G.height))
    a_bg = pygame.Surface((2 * G.width, G.height))

    tiles = [pygame.image.load("./assets/dirt1.png"),
             pygame.image.load("./assets/dirt2.png"),
             pygame.image.load("./assets/dirt3.png"),
             pygame.image.load("./assets/dirt-simple.png")]

    for i in range(50):
        for j in range(15):
            t = pygame.transform.scale(random.choice(tiles), (60, 60))
            img = pygame.transform.rotate(t, round(random.randint(0, 3)) * 90)
            u_bg.blit(img, (i * 60, j * 60, 60, 60))

    tile = pygame.transform.scale(pygame.image.load("./assets/grass1.png"), (60, 60))
    rivertile = pygame.transform.scale(pygame.image.load("./assets/river1.png"), (60, 60))
    rivertile2 = pygame.transform.scale(pygame.image.load("./assets/river2.png"), (60, 60)) # todo: not going into river

    for i in range(48):
        for j in range(15):
            if round(random.random()):
                a_bg.blit(pygame.transform.flip(tile, True, False), (i * 60, j * 60, 60, 60))
            else:
                a_bg.blit(tile, (i * 60, j * 60, 60, 60))

    for j in range(15):
        a_bg.blit(rivertile, (48 * 60, j * 60, 60, 60))
    for j in range(15):
        a_bg.blit(rivertile2, (49 * 60, j * 60, 60, 60))

    playing = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0, {}
        if underground and not playing:
            pygame.mixer.music.load('./assets/music/underground-loop.wav')
            pygame.mixer.music.play(-1)
            playing = True
        elif not underground and not playing:
            pygame.mixer.music.load('./assets/music/aboveground-loop.wav')
            pygame.mixer.music.play(-1)
            playing = True

        # Checking for switiching sides
        if pygame.mouse.get_pressed(3)[0]:
            if rat.near_mouse() and near_exit(exits, rat):
                underground = not underground
                playing = False
                for rock in a_rocks:
                    rock.update_image(underground)
                time.sleep(0.25)
            else:
                # check for material
                if underground:
                    for obj in group_u_mats.sprites():
                        if pygame.sprite.collide_rect(ratrect, obj):
                            total_iron += obj.value
                            group_u_mats.remove(obj)
                else:
                    for obj in group_a_mats.sprites():
                        if pygame.sprite.collide_rect(ratrect, obj):
                            rat.energy = min(rat.max_energy, rat.energy + (obj.value + 1) * 50)
                            group_a_mats.remove(obj)

        if underground:
            screen.blit(u_bg, (-screen_offset, 0, 1500, 900))
        else:
            if update_counter % 29 == 0 and round(random.random()):
                for i in range(48):
                    for j in range(15):
                        if round(random.random() * 4 - 4):
                            a_bg.blit(pygame.transform.flip(tile, True, False), (i * 60, j * 60, 60, 60))
                        else:
                            a_bg.blit(tile, (i * 60, j * 60, 60, 60))
                for j in range(15):
                    a_bg.blit(rivertile, (48 * 60, j * 60, 60, 60))
                for j in range(15):
                    a_bg.blit(rivertile2, (49 * 60, j * 60, 60, 60))

            screen.blit(a_bg, (-screen_offset, 0, 1500, 900))

        px, py = rat.get_mouth()
        mx, my = pygame.mouse.get_pos()

        ratrect = Temp(px, py)
        mouserect = Temp(mx, my)

        if underground:
            # Update tree
            for obj in trees:
                obj.drawroots(update_counter)

            group_underground.draw(screen)
            group_u_mats.draw(screen)

            # the root depth if mouse is currently hovering over one
            group_root.update()
            collided_root = pygame.sprite.spritecollideany(mouserect, group_root)

            if collided_root is None:
                hover_root_depth = 0
            else:
                hover_root_depth = collided_root.depth

            if pygame.mouse.get_pressed(3)[0]:
                if rat.near_mouse() and hover_root_depth > 0:
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
                                         (round(rat.x - screen_offset) - rat.image.get_width() // 2,
                                          round(rat.y) - rat.image.get_height()),
                                         (round(
                                             rat.x - screen_offset - rat.image.get_width() // 2 + rat.image.get_width() * (
                                                     chopping_meter / required_power[hover_root_depth])),
                                          round(rat.y) - rat.image.get_height()), 10)

                    if chopping_meter > required_power[hover_root_depth]:
                        chopping_meter = 0
                        for i in trees:
                            wood_obtained = i.trim(chopping_location[0] + screen_offset, chopping_location[1])
                            if wood_obtained > 0:
                                display_text.append(
                                    Text(round(rat.x - screen_offset) - rat.image.get_width() / 4,
                                         round(rat.y) - rat.image.get_height(),
                                         f"+{wood_obtained}", 60, screen))
                            # pygame.draw.circle(screen, "red", (px,py), 10) # makes the rat looks like a clown
                            total_wood += wood_obtained
            else:
                chopping_meter = 0

            if near_nest(nests, rat):
                # rat.energy = min(rat.max_energy, rat.energy + G.energy_recharge_regen)
                rat.stamina = min(rat.max_stamina, rat.stamina + G.stamina_recharge_regen)

            if hover_root_depth > 0:
                pygame.draw.circle(screen, power_colour[hover_root_depth],
                                   (collided_root.x - screen_offset, collided_root.y), 10)

            rat.turn(pygame.mouse.get_pos())  # I still want this to be before move

            for obs in group_u_obstacles.sprites():
                if pygame.sprite.collide_circle(ratrect, obs):
                    # b = obs.boundaries
                    # if b[0] <= px <= b[2] and b[1] <= py <= b[3]:
                    rat.stamina = min(rat.max_stamina, rat.stamina + G.idle_stamina_regen)
                    break
            else:
                if pygame.sprite.spritecollideany(ratrect, group_root) is not None:
                    rat.move(rat.stamina / rat.max_stamina + 0.2)
                else:
                    rat.move(rat.spd)
        else:
            # Update tree
            for obj in trees:
                obj.drawroots(update_counter)

            group_aboveground.draw(screen)
            group_a_mats.draw(screen)

            rat.turn(pygame.mouse.get_pos())

            for obs in group_a_obstacles.sprites():
                if pygame.sprite.collide_circle(ratrect, obs):
                    # b = obs.boundaries
                    # if b[0] <= px <= b[2] and b[1] <= py <= b[3]:
                    rat.stamina = min(rat.max_stamina, rat.stamina + G.idle_stamina_regen)
                    break
            else:
                rat.move(rat.spd)

            if rat.x > 2 * G.width - 150:
                # River:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        # spd
                        if event.key == pygame.K_1 and total_wood >= 2 ** rat.upgrade_level[1][0]:
                            rat.upgrade_level[1][0] = min(5, rat.upgrade_level[1][0] + 1)
                            total_wood -= 2 ** rat.upgrade_level[1][0]


        if len(display_text) > 0:
            img = pygame.transform.scale(pygame.image.load("./assets/wood_1fab5.png"), (50, 50))
            screen.blit(img,
                        (display_text[0].x - screen_offset - rat.image.get_width() / 4,
                         display_text[0].y - rat.image.get_height() / 4))  # TODO check
            display_text[0].draw("white", 30)
            wood_colour = "green"
        else:
            wood_colour = "white"

        rat.energy -= rat.energy_cost

        for obj in trees:
            obj.draw()

        # for obj in trees:
        #     obj.update()
        # for obj in aboveground_objects:
        #     obj.update()
        # for obj in underground_objects:
        #     obj.update()
        group_all.update()

        if update_counter >= G.root_counter_max:
            for i in trees:
                i.extend()
            update_counter = 0

        ## Status displays
        # wood counter
        img = pygame.transform.scale(pygame.image.load("./assets/wood_1fab5.png"), (50, 50))
        screen.blit(img, (100, 35, 50, 50))
        wood = Text(35, 50, f"Wood:   {total_wood}", 99, screen)
        wood.draw(wood_colour, 30)

        # energy
        e_img = pygame.transform.scale(pygame.image.load("./assets/energy.png"), (20, 30))
        energy = Text(35, 100, f"Energy    : {round(rat.energy)}", 99, screen)
        color = ["red", "yellow", "green"][max(0, round(rat.energy * 3 / rat.max_energy) - 1)]
        energy.draw(color, 30)
        screen.blit(e_img, (105, 95, 20, 30))

        # stamina bar
        color = ["red", "yellow", "green"][max(0, round(rat.stamina * 3 / rat.max_stamina) - 1)]
        pygame.draw.rect(screen, "black", pygame.Rect(34, 139, round((rat.max_stamina - 1) / 2) + 2, 32), 1)
        pygame.draw.rect(screen, color, pygame.Rect(35, 140, round(max(0, round(rat.stamina - 1)) / 2), 30))

        # stamina text
        stam = Text(115, 145, f"Stamina", 99, screen)
        stam.draw("black", 30)

        if near_nest(nests, rat):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # spd
                    if event.key == pygame.K_1 and total_wood >= 2 ** rat.upgrade_level[1][0]:
                        total_wood -= 2 ** rat.upgrade_level[1][0]
                        rat.upgrade_level[1][0] = min(5, rat.upgrade_level[1][0] + 1)
                    # moving cost
                    elif event.key == pygame.K_2 and total_wood >= 2 ** rat.upgrade_level[2][0]:
                        total_wood -= 2 ** rat.upgrade_level[2][0]
                        rat.upgrade_level[2][0] = min(5, rat.upgrade_level[2][0] + 1)
                    # max stamina
                    elif event.key == pygame.K_3 and total_wood >= 2 ** rat.upgrade_level[3][0]:
                        total_wood -= 2 ** rat.upgrade_level[3][0]
                        rat.upgrade_level[3][0] = min(5, rat.upgrade_level[3][0] + 1)
                    # stamina regen
                    elif event.key == pygame.K_4 and total_wood >= 2 ** rat.upgrade_level[4][0]:
                        total_wood -= 2 ** rat.upgrade_level[4][0]
                        rat.upgrade_level[4][0] = min(5, rat.upgrade_level[4][0] + 1)
                    # energy cost
                    elif event.key == pygame.K_5 and total_wood >= 2 ** rat.upgrade_level[5][0]:
                        total_wood -= 2 ** rat.upgrade_level[5][0]
                        rat.upgrade_level[5][0] = min(5, rat.upgrade_level[5][0] + 1)


            box = pygame.Surface((300, 400))
            box.fill(G.box_colour)
            screen.blit(box, (0, 250))
            pygame.draw.rect(screen, G.border_colour, pygame.Rect(0, 250, 300, 400), 10)
            trunk = pygame.transform.scale(pygame.image.load("./assets/wood_1fab5.png"), (75, 75))

            left = 10
            top = 260

            upgrade_text_names = ['SPD', 'MOVE COST', 'MAX STAM', 'STAM REGEN', 'ENERGY COST']

            locations = []
            for i in range(5):
                locations.append((left, top + i * 76))
                screen.blit(trunk, (left + 200, top + i * 76))

            for i in range(len(locations)):
                index = locations[i]
                t = Text(index[0] + 75 / 8, index[1] + 75 / 4, f"{upgrade_text_names[i]}", 999, screen)
                t.draw("white", 35)
                t2 = Text(index[0] + 75 / 4, index[1] + 75 / 2 + 75 / 8, f"Lv. {rat.upgrade_level[i + 1][0]}", 999, screen)
                t2.draw("white", 30)
                t3 = Text(index[0] + 225, index[1] + 75 / 4 + 75 / 8, f"{2 ** rat.upgrade_level[1 + i][0]}", 999, screen)
                t3.draw("white", 50)

        ## Loop updates
        for text in display_text:
            if text.timeleft <= 0:
                display_text.remove(text)

        update_counter += 1
        pygame.display.flip()
        clock.tick(60)

        if rat.energy <= 0:
            screen.blit(u_bg, (-screen_offset, 0, 1500, 900))
            return 4, {"won": False} # game over
