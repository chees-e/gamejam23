import pygame
import pygame_menu

from scenes import menu


# RV:
# next scene, next scenes parameters
# Entry point
def run(screen, params, page):
    while True:
        tutorial = pygame_menu.Menu('', 1500, 900, theme=mainmenu)
        if page==0:
            tutorial.add.label('Welcome to NYYK’S BIZZARE ADVENTURE! '
                               'Nyyk has woken up in a mysterious burrow, '
                               'surrounded by trees that seem keen on trapping it underground... '
                               'forever. '
                               'Fight back the tree roots and help Nyyk find its way out of this place',
                               wordwrap=True, font_name=pygame_menu.font.FONT_MUNRO)
        else:
            tutorial.add.label(tutoriallabel[page])
            tutorial.add.label(tutoriallabel2[page], wordwrap=True, font_name=pygame_menu.font.FONT_MUNRO)
            tutorial.add.image(tutorialimages[page])
        tutorial.add.button('PREVIOUS', prev, screen, page)
        tutorial.add.button('NEXT', next, screen, page)
        tutorial.add.button('Back', back, screen)

        tutorial.mainloop(surface)


# init pygame
pygame.init()
surface = pygame.display.set_mode((1500, 900))
tutorialimages=['./assets/dirt1.png',
                './assets/dirt1.png',
                './assets/dirt2.png',
                './assets/dirt3.png',
                './assets/wood_1fab5.png',
                './assets/wood_1fab5.png',
                './assets/grass1.png',
                './assets/apple.png',
                './assets/river1.png']
tutoriallabel=['', '1. MOVEMENT', '2. CHEW THROUGH ROOTS', '3. DEFEND YOUR NEST', '4. COLLECT WOOD', '5. UPGRADE STATS', '6. TOUCH GRASS', '7. FIND FOOD', '8. CROSS THE RIVER' ]
tutoriallabel2=['', 'Your rodent will follow your mouse cursor. Keep an eye on your Stamina bar!',
                'Click and hold to begin chewing through the root. Thicker roots take longer to chew through. ',
                'Once the roots destroy your nest, you can no longer regen your Stamina there. Keep the roots at bay.',
                'Each root you chew through has the chance to drop 0-2 pieces of wood. ',
                'As a highly intelligent rodent, you can upgrade yourself while in your nest - use wood to upgrade your stats to help you break the roots faster.',
                'Visit the outside world by clicking on a tunnel.',
                'While above ground, you can collect food that will replenish your energy. Be careful, though - the roots will keep growing while you’re above ground! And when you run out of energy, it’s Game Over',
                'Build a bridge and win the game!']

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
    if page==8:
        return
    else:
        page = page + 1
        run(screen, {}, page)
        return


def back(screen):
    menu.run(screen, {})
    return
