import pygame
import pygame_menu

from scenes import menu


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):
    while True:
        settings = pygame_menu.Menu('', 1500, 900, theme=mainmenu)

        settings.add.button('Volume', volume, screen)
        settings.add.button('Back', back, screen)

        settings.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))

mainmenu = pygame_menu.themes.THEME_DEFAULT.copy()
mainmenu.background_color = (4,4,4) #set theme background color as the image
mainmenu.widget_font = pygame_menu.font.FONT_8BIT
mainmenu.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
mainmenu.widget_margin = (0, 30)
mainmenu.widget_padding = 10
mainmenu.widget_font_color = (255, 255, 255)
mainmenu.widget_selection_effect = pygame_menu.widgets.RightArrowSelection(arrow_size=(30, 40))

# define buttons
def volume(screen):
    print("open volume settings")
    return


def back(screen):
    menu.run(screen, {})
    return
