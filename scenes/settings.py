import pygame
import pygame_menu

from scenes import menu


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):
    while True:
        settings = pygame_menu.Menu('', 1500, 900, theme=settings_bg)

        settings.add.button('Volume', volume, screen)
        settings.add.button('Back', back, screen)

        settings.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))

settings_bg = pygame_menu.themes.THEME_DEFAULT.copy()

settings_bg.background_color = pygame_menu.baseimage.BaseImage(
    image_path="./assets/menu_bg.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
    drawing_offset=(0, 0)
)
settings_bg.widget_font = pygame_menu.font.FONT_8BIT
settings_bg.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
settings_bg.widget_margin = (0, 30)
settings_bg.widget_padding = 10
settings_bg.widget_font_color = (255, 255, 255)
settings_bg.widget_selection_effect = pygame_menu.widgets.RightArrowSelection(arrow_size=(30, 40))


# define buttons
def volume(screen):
    print("open volume settings")
    return


def back(screen):
    menu.run(screen, {})
    return
