import pygame
import pygame_menu

from scenes import menu


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params, page):
    while True:
        tutorial = pygame_menu.Menu('', 1500, 900, theme=mainmenu)
        tutorial.add.image(tutorialimages[page])
        tutorial.add.button('PREVIOUS', prev, screen, page)
        tutorial.add.button('NEXT', next, screen, page)
        tutorial.add.button('Back', back, screen)

        tutorial.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))
tutorialimages=['./assets/dirt1.png', './assets/dirt2.png', './assets/dirt3.png']

mainmenu = pygame_menu.themes.THEME_DEFAULT.copy()
mainmenu.background_color = (4,4,4) #set theme background color as the image
mainmenu.widget_font = pygame_menu.font.FONT_8BIT
mainmenu.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
mainmenu.widget_margin = (0, 30)
mainmenu.widget_padding = 10
mainmenu.widget_font_color = (255, 255, 255)
mainmenu.widget_selection_effect = pygame_menu.widgets.RightArrowSelection(arrow_size=(30, 40))

# define buttons
def prev(screen, page):
    print(page)
    if page==0:
        return
    else:
        page = page - 1
        run(screen, {}, page)
        return

def next(screen, page):
    print(page)
    page = page + 1
    run(screen, {}, page)
    return page


def back(screen):
    menu.run(screen, {})
    return
