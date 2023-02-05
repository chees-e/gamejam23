import pygame
import random

import util.const as G
from scenes import menu, game, credits_page, gameend


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.scenes = [
            menu,
            game,
            credits_page,
            gameend
        ]

        print("Game started")

    def run(self):
        menu.run(self.screen, {})
        # params = {}
        # next_scene = 0
        # while True:
        #     print("SCENE", next_scene)
        #     next_scene, params = self.scenes[next_scene].run(self.screen, params)


def main():
    pygame.init()

    pygame.display.set_caption("Insert game name")
    screen = pygame.display.set_mode(G.size)
    # add other screen initialization
    screen.fill(G.bg_colour)

    pygame.display.flip()

    # input()

    g = Game(screen)
    g.run()


if __name__ == "__main__":
    main()
    pygame.quit()
