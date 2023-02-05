import pygame
import util.const as G


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

            render = pygame.font.SysFont(None, 160).render("Game Over", True, "maroon")

            screen.blit(render, (G.width // 2 - render.get_width() // 2, G.height // 2 - render.get_height() // 2))

            render = pygame.font.SysFont(None, 80).render("Click anywhere to Continue", True, "maroon")

            screen.blit(render, (G.width // 2 - render.get_width() // 2, G.height // 2 - render.get_height() + 160))

            pygame.display.flip()
            clock.tick(60)

        return 0, {}
