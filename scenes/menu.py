import pygame
import util.const as G
import pygame_menu

# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):
    while True:
        input("IN menu")
        return 1, {}

# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))

#define buttons
def start():
    # idk
    pass

def settings():
    #open the settings menu
    pass

def credits():
    #open the credits page
    pass

menu = pygame_menu.Menu('', 1500, 900)

menu.add.image('../assets/onlyclowns_transparent.png', scale=(0.5, 0.5))
menu.add.button('Play', start)
menu.add.button('Settings', settings)
menu.add.button('Credits', credits)
menu.add.button('Quit', pygame_menu.events.EXIT) #letsfuckinggoooo

menu.mainloop(surface)