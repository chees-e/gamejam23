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

extend_chance = 0.8
wood_double_chance = 0.1
wood_lost_chance = 0.3

energy_lost = 0.01
energy_recharge_regen = 1

chopping_stamina_cost_base = 1
moving_stamina_cost = 0.4
idle_stamina_regen = 0.2
stamina_recharge_regen = 5

hitbox_scale = 4

trail_colour = "#1c1a1a" #TODO select better colour
text_colour = "black"
bg_colour = "white"

collision_thres = 20 # distance sqaured