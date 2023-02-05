import pygame
import pygame_menu

from scenes import menu


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):
    while True:
        settings = pygame_menu.Menu('', 1500, 900)

        settings.add.button('Volume', volume, screen)
        settings.add.button('Back', back, screen)

        settings.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))