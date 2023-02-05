import pygame
import pygame_menu

from scenes import game, settings, credits_page


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):

    while True:
        menu = pygame_menu.Menu('', 1500, 900, theme=mainmenu)

        # menu.add.image('./assets/onlyclowns_transparent.png', scale=(0.5, 0.5))
        menu.add.button('Play', start, screen)
        menu.add.button('Tutorial', go_to_tutorial, screen)
        menu.add.button('Settings', go_to_settings, screen)
        menu.add.button('Credits', go_to_credits, screen)
        menu.add.button('Quit', pygame_menu.events.EXIT)  # letsfuckinggoooo

        menu.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))

# create custom theme
mainmenu = pygame_menu.themes.THEME_DEFAULT.copy() #copy default theme
mmbg = pygame_menu.baseimage.BaseImage(
    image_path="./assets/title-screen.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
    drawing_offset=(0, 0)
)
mainmenu.background_color = mmbg #set theme background color as the image
mainmenu.widget_font = pygame_menu.font.FONT_8BIT
mainmenu.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
mainmenu.widget_margin = (0, 30)
mainmenu.widget_padding = 10
mainmenu.widget_font_color = (255, 255, 255)
mainmenu.widget_selection_effect = pygame_menu.widgets.RightArrowSelection(arrow_size=(30, 40))


# define buttons
def start(screen):
    game.run(screen, {})
    return

def go_to_tutorial(screen):
    #tutorial page
    pass

def go_to_settings(screen):
    settings.run(screen, {})
    pass


def go_to_credits(screen):
    credits_page.run(screen, {})
    pass
