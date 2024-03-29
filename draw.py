import pygame as pg
import container
from stopwatch import Stopwatch
import mouse
import calculations

pg.init()
sw = Stopwatch()
sw.reset()
calc = calculations.CalculateEv()
ms = mouse.HandleMouse()


class DrawOnTheScreen(container.Container):
    def __init__(self):
        super().__init__()

    def draw_the_grid(self):
        grid_rects = []
        y = 0
        for _ in range(self.scr_height // self.rect_size):
            for x in range(self.scr_width // self.rect_size):
                rect = pg.draw.rect(self.screen, self.color_green,
                                    (x * self.rect_size, y, self.rect_size, self.rect_size), 2)
                grid_rects.append(rect)
                if x * self.rect_size >= self.scr_width - self.rect_size:
                    y += self.rect_size
        return grid_rects

    def draw_circles(self, grid_rects, draw_for_ai, index_for_ai):
        circles = []
        if not draw_for_ai and self.circles_on_the_screen in [self.crosses_on_the_screen - 1, self.crosses_on_the_screen]:
            for index, rect in enumerate(grid_rects):
                if ms.check_mouse_pos(rect) and ms.check_button_clicked(2):
                    circle = pg.draw.circle(self.screen, self.color_blue, rect.center, rect.size[0] // 2,
                                            rect.size[1] // 2)
                    circles.append(index)
                    self.circles_on_the_screen += 1
                    calc.replace_in_map(index, 'ci')
                    break
        if draw_for_ai:
            circle = pg.draw.circle(self.screen, self.color_blue, grid_rects[index_for_ai].center,
                                    grid_rects[index_for_ai].size[0] // 2,
                                    grid_rects[index_for_ai].size[1] // 2)
            circles.append(index_for_ai)
            # self.circles_on_the_screen += 1
            calc.replace_in_map(index_for_ai, 'ci')
        return circles

    def draw_crosses(self, grid_rects, draw_for_ai, index_for_ai):
        crosses = []
        cross = []
        if not draw_for_ai and self.crosses_on_the_screen in [self.circles_on_the_screen - 1, self.circles_on_the_screen]:
            for index, rect in enumerate(grid_rects):
                if ms.check_mouse_pos(rect) and ms.check_button_clicked(0):
                    cross.extend((pg.draw.line(self.screen, self.color_blue, rect.topleft, rect.bottomright, 8), pg.draw.line(self.screen, self.color_blue, rect.topright, rect.bottomleft, 8)))

                    crosses.append(index)
                    # self.crosses_on_the_screen += 1
                    calc.replace_in_map(index, 'cr')
                    break
        if draw_for_ai:
            cross.extend((pg.draw.line(self.screen, self.color_blue, grid_rects[index_for_ai].topleft, grid_rects[index_for_ai].bottomright, 8), pg.draw.line(self.screen, self.color_blue, grid_rects[index_for_ai].topright, grid_rects[index_for_ai].bottomleft, 8)))

            crosses.append(index_for_ai)
            # self.crosses_on_the_screen += 1
            calc.replace_in_map(index_for_ai, 'cr')
        return crosses

    def draw_the_winning_five(self, winner_cross, winner_circle, circles, crosses, grid_rects):
        if winner_circle:

            indexes = calc.find_if_winning(True, self.rect_limit,return_indexes=True)
            for x in indexes:
                pg.draw.rect(self.screen, self.color_white, (grid_rects[x]), 6)
            self.game_won_by_circles = True

        if winner_cross:
            indexes = calc.find_if_winning(False, self.rect_limit,return_indexes=True)
            for x in indexes:
                pg.draw.rect(self.screen, self.color_white, (grid_rects[x]), 6)
            self.game_won_by_crosses = True
