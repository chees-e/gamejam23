import pygame
import pygame_menu

from scenes import game, settings, credits_page, tutorial


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):
    pygame.mixer.music.load("./assets/music/lobby.wav")
    pygame.mixer.music.play(-1)
    while True:
        menu = pygame_menu.Menu('', 1500, 900, theme=menu_bg)

        # menu.add.image('./assets/onlyclowns_transparent.png', scale=(0.5, 0.5))
        menu.add.button('Play', start, screen, font_size=50)
        menu.add.button('How To Play', go_to_tutorial, screen)
        menu.add.button('Settings', go_to_settings, screen)
        menu.add.button('Credits', go_to_credits, screen)
        menu.add.button('Quit', pygame_menu.events.EXIT)  # letsfuckinggoooo

        menu.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))

# create custom theme
menu_bg = pygame_menu.themes.THEME_DEFAULT.copy()  # copy default theme
mmbg = pygame_menu.baseimage.BaseImage(
    image_path="./assets/title-screen.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
    drawing_offset=(0, 0)
)
menu_bg.background_color = mmbg  # set theme background color as the image
menu_bg.widget_font = pygame_menu.font.FONT_8BIT
menu_bg.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
menu_bg.widget_margin = (0, 30)
menu_bg.widget_padding = 10
menu_bg.widget_font_color = (255, 255, 255)
menu_bg.widget_selection_effect = pygame_menu.widgets.RightArrowSelection(arrow_size=(30, 40))


# define buttons
def start(screen):
    game.run(screen, {})
    return


def go_to_tutorial(screen):
    # tutorial page
    tutorial.run(screen, {})
    pass


def go_to_settings(screen):
    settings.run(screen, {})
    pass


def go_to_credits(screen):
    credits_page.run(screen, {})
    pass
