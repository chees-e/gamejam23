import pygame
import pygame_menu

from scenes import menu


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):
    while True:
        credits = pygame_menu.Menu('', 1500, 900, theme=credits_bg)

        credits.add.image('./assets/onlyclowns.png', scale=(0.5,0.5))
        credits.add.label('programming - ricky , shawn , nick')
        credits.add.label('music - ricky')
        credits.add.label('art - jean')
        credits.add.button('Back', back, screen, font_name=pygame_menu.font.FONT_8BIT)

        credits.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))

credits_bg = pygame_menu.themes.THEME_DEFAULT.copy()
credits_bg.background_color = pygame_menu.baseimage.BaseImage(
    image_path="./assets/menu-bg.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
    drawing_offset=(0, 0)
)
credits_bg.widget_font = pygame_menu.font.FONT_MUNRO
credits_bg.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
credits_bg.widget_margin = (0, 10)
credits_bg.widget_padding = 10
credits_bg.widget_font_color = (255, 255, 255)
credits_bg.widget_selection_effect = pygame_menu.widgets.RightArrowSelection(arrow_size=(30, 40))

def back(screen):
    menu.run(screen, {})
    return