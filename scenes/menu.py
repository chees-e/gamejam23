import pygame
import pygame_menu

from scenes import game, settings, credits_page


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):

    while True:
        menu = pygame_menu.Menu('', 1500, 900)

        menu.add.image('./assets/onlyclowns_transparent.png', scale=(0.5, 0.5))
        menu.add.button('Play', start, screen)
        menu.add.button('Settings', go_to_settings, screen)
        menu.add.button('Credits', go_to_credits, screen)
        menu.add.button('Quit', pygame_menu.events.EXIT)  # letsfuckinggoooo

        menu.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))


# define buttons
def start(screen):
    game.run(screen, {})
    return


def go_to_settings(screen):
    settings.run(screen, {})
    pass


def go_to_credits(screen):
    credits_page.run(screen, {})
    pass
