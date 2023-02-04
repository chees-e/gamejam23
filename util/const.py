import random

import pygame

size = width, height = 1500, 900

ratsize = rat_width, rat_height = 50, 50

root_counter_max = 29

root_colour = (105, 65, 48)
root_thickness = 20
root_maxlength = 20
root_speed = 5

extend_chance = 0.8
wood_double_chance = 0.1
wood_lost_chance = 0.3

energy_lost = 0.01
energy_recharge_regen = 1

chopping_stamina_cost_base = 2
moving_stamina_cost = 2
idle_stamina_regen = 1
stamina_recharge_regen = 5

font_size = 24

trail_colour = "brown" #TODO select better colour
text_colour = "black"
bg_colour = "white"

collision_thres = 20 # distance sqaured