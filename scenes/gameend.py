import pygame
import util.const as G
import util.getpath as P

from scenes import menu, game, credits_page, gameend

# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):
    won = params['won']
    pygame.init()
    print("GGGGGGGGG")
    clock = pygame.time.Clock()

    if not won:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0, {}
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return 0, {}

            worry = pygame.transform.scale(pygame.image.load(P.get("./assets/worryrat.png")), (900, 900))
            box = pygame.Surface((1500, 900))
            box.fill("black")
            screen.blit(box, (0, 0, 1500, 900))
            screen.blit(worry, (300, 0, 900, 900))

            render = pygame.font.SysFont(None, 80).render("Game Over, you are going to Alberta", True, "red")

            screen.blit(render, (G.width // 2 - render.get_width() // 2, G.height // 2 - render.get_height() // 2))

            render = pygame.font.SysFont(None, 40).render("Click anywhere to Continue", True, "red")

            screen.blit(render, (G.width // 2 - render.get_width() // 2, G.height // 2 - render.get_height() + 160))

            pygame.display.flip()
            clock.tick(60)
    else:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0, {}
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return 0, {}
            render = pygame.font.SysFont(None, 80).render("You are going to Ohio!", True, "white")

            screen.blit(render, (G.width // 2 - render.get_width() // 2, G.height // 2 - render.get_height() // 2))

            render = pygame.font.SysFont(None, 40).render("Click anywhere to Continue", True, "white")

            screen.blit(render, (G.width // 2 - render.get_width() // 2, G.height // 2 - render.get_height() + 160))

            pygame.display.flip()
            clock.tick(60)

        return 0, {}
