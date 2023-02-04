import pygame
import random

import util.const as G
from scenes import menu, game

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.scenes = [
            menu,
            game
        ]

        print("Game started")

    def run(self):
        next_scene = 1
        params = {}
        while True:
            next_scene, params = self.scenes[next_scene].run(self.screen, params)


def main():
    pygame.init()

    pygame.display.set_caption("Insert game name")
    screen = pygame.display.set_mode(G.size)
    # add other screen intialization
    screen.fill(G.bg_colour)

    pygame.display.flip()

    input()

    g = Game(screen)
    g.run()



if __name__ == "__main__":
    main()
    pygame.quit()
