import random

import pygame

size = width, height = 1500, 900

ratsize = rat_width, rat_height = 50, 50

root_counter_max = 29

root_colours = [
    (60, 45, 40)
]

root_thickness = 20
root_maxlength = 20
root_speed = 5

# For now Ill just have 1 tile around the border of no sprites
tiles_x = 8
tiles_y = 5
max_tiles = (tiles_x-2) * (tiles_y-2)
tiles_width = width//tiles_x
tiles_height = height//tiles_y
tile_offset = 50 # 2*offset = min distance between two sprites

extend_chance = 0.8
wood_double_chance = 0.1
wood_lost_chance = 0.3

energy_lost = 0.01
energy_recharge_regen = 1

chopping_stamina_cost_base = 1
moving_stamina_cost = 0 # 0.5
idle_stamina_regen = 0.5
stamina_recharge_regen = 5

hitbox_scale = 2.5

proximity_value = 100


trail_colour = "#1c1a1a" #TODO select better colour
text_colour = "black"
bg_colour = "white"

collision_thres = 20 # distance sqaured