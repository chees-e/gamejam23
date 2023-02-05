import pygame
import pygame_menu

from scenes import menu


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params):
    while True:
        credits = pygame_menu.Menu('', 1500, 900, theme=mainmenu)

        credits.add.image('./assets/onlyclowns.png', scale=(2,2))
        credits.add.label('programming - ricky , shawn , nick')
        credits.add.label('music - ricky')
        credits.add.label('art - jean')
        credits.add.button('Back', back, screen, font_name=pygame_menu.font.FONT_8BIT)

        credits.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))

mainmenu = pygame_menu.themes.THEME_DEFAULT.copy()
mainmenu.background_color = (4,4,4)
mainmenu.widget_font = pygame_menu.font.FONT_MUNRO
mainmenu.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
mainmenu.widget_margin = (0, 10)
mainmenu.widget_padding = 10
mainmenu.widget_font_color = (255, 255, 255)
mainmenu.widget_selection_effect = pygame_menu.widgets.RightArrowSelection(arrow_size=(30, 40))

def back(screen):
    menu.run(screen, {})
    return