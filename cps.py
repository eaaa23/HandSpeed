import pygame as pg
from pygame.constants import *
from time import time
pg.init()

FONT = pg.font.SysFont("Arial", 30)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 200

BLACK = (0, 0, 0)
RED = (255, 0, 0)
DRAW_POSITION = [(0, 100), (500, 100)]
LABEL_TEXT = "Clicks per second: "
LABEL_POSITION = (300, 0)
LABEL_COLOR = (0, 0, 200)

FLASH_INTERVAL = 0.3
BUTTON2KEY = {1: 0,  # left
              3: 1}  # right
TIP_TEXT = ["LEFT: ", "RIGHT: "]
TITLE = "Click it!"


def draw_text(screen, pos, text, color=(0, 0, 0)):
    surf = FONT.render(text, True, color)
    screen.blit(surf, pos)
    return surf.get_rect()


def clear_screen(screen, color=RED):
    screen.fill(color)


def trans_button(btn):
    return (btn-1) // 2


def main():
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption(TITLE)
    last_press = [time()] * 2
    this_press = [time()] * 2
    cps = [0, 0]
    clear_screen(screen)
    pg.display.update()
    while True:
        do_draw = False
        moved_mouse = False
        for evt in pg.event.get():
            if evt.type == QUIT:
                pg.quit()
                return
            else:
                if evt.type == MOUSEBUTTONDOWN:
                    if evt.button not in BUTTON2KEY:
                        continue
                    key = BUTTON2KEY[evt.button]
                    this_press[key] = time()
                    cps[key] = 1 / (this_press[key] - last_press[key])
                    last_press[key] = this_press[key]
                    do_draw = True
                    moved_mouse = True
        if not moved_mouse:
            for key in range(2):
                if time()-last_press[key] > FLASH_INTERVAL:
                    cps[key] = 0
                    do_draw = True
        if do_draw:
            clear_screen(screen)
            draw_text(screen, LABEL_POSITION, LABEL_TEXT, LABEL_COLOR)
            for pos, num, tiptx in zip(DRAW_POSITION, cps, TIP_TEXT):
                draw_text(screen, pos, tiptx + str(round(num)))
        pg.display.update()


if __name__ == '__main__':
    main()
