from textual.widget import Widget
from typing import Dict
from maze_generator.maze import Maze
from textual.containers import Horizontal, Vertical, HorizontalGroup
from textual.widgets import Static
from textual.app import ComposeResult
from textual_canvas import Canvas

from textual.color import Color

from maze_generator.maze_generator import MazeGenerator


class MyCanvas(Canvas):
    def __init__(self, nb_row: int, nb_col: int, colours: Dict[str, Color]):
        super().__init__(
            width=(nb_col * 3 + (nb_col + 1)),
            height=(nb_row * 3 + (nb_row + 1)),
            # Background is managed in the css
            # canvas_color=colours["background"],
            # canvas_color=colours["background"],
            # canvas_color=colours["secondary"],
        )
        self.__colours = colours

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours: Dict[str, Color]):
        self.__colours = colours

    # ########################################################################
    # ############################################################## DRAW ####
    def __draw_line(self, row: int, col: int, vertical: bool = False):
        if vertical:
            self.draw_line(
                col, row, col, row + 2, color=self.__colours["primary"]
            )
        else:
            self.draw_line(
                col, row, col + 2, row, color=self.__colours["primary"]
            )

    def __draw_square(self, row, col):
        self.__draw_line(row - 1, col - 1)
        self.__draw_line(row, col - 1)
        self.__draw_line(row + 1, col - 1)

    # ########################################################################
    # ######################################################### DIG HOLES ####
    def dig_holes(self, maze_hexa: Maze):
        """
        Loop in the given maze and draw where it's open.

                     0               1               2

                 0   1   2   3   4   5   6   7   8   9  10

               ┏━━━┳━━━┳━━━┓   ┏━━━┳━━━┳━━━┓   ┏━━━┳━━━┳━━━┓
            0  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
               ┣━━━╋━━━╋━━━┫   ┣━━━╋━━━╋━━━┫   ┣━━━╋━━━╋━━━┫
        0   1  ┃   ┃ X ┃   ┃   ┃   ┃ X ┃   ┃   ┃   ┃ X ┃   ┃
               ┣━━━╋━━━╋━━━┫   ┣━━━╋━━━╋━━━┫   ┣━━━╋━━━╋━━━┫
            2  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
               ┗━━━┻━━━┻━━━┛   ┗━━━┻━━━┻━━━┛   ┗━━━┻━━━┻━━━┛
            3
               ┏━━━┳━━━┳━━━┓   ┏━━━┳━━━┳━━━┓   ┏━━━┳━━━┳━━━┓
            4  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
               ┣━━━╋━━━╋━━━┫   ┣━━━╋━━━╋━━━┫   ┣━━━╋━━━╋━━━┫
        1   5  ┃   ┃ X ┃   ┃   ┃   ┃ X ┃   ┃   ┃   ┃ X ┃   ┃
               ┣━━━╋━━━╋━━━┫   ┣━━━╋━━━╋━━━┫   ┣━━━╋━━━╋━━━┫
            6  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
               ┗━━━┻━━━┻━━━┛   ┗━━━┻━━━┻━━━┛   ┗━━━┻━━━┻━━━┛
        """

        # Loop in the maze draw where it's open
        for rh, row_hexa in enumerate(maze_hexa.values):
            for ch, cell_hexa in enumerate(row_hexa):
                # Get the middle coordinate in self.cells
                row = (rh * 4) + 2
                col = (ch * 4) + 2

                if cell_hexa & 0b1111 != 0b1111:
                    self.__draw_square(row, col)

                if cell_hexa & 0b0001 != 0b0001:  # Top
                    self.__draw_line(row - 2, col - 1)
                if cell_hexa & 0b0100 != 0b0100:  # Bottom
                    self.__draw_line(row + 2, col - 1)
                if cell_hexa & 0b1000 != 0b1000:  # Left
                    self.__draw_line(row - 1, col - 2, vertical=True)
                if cell_hexa & 0b0010 != 0b0010:  # Right
                    self.__draw_line(row - 1, col + 2, vertical=True)


class CMaze(Widget):
    def __init__(self, config, colours: Dict[str, Color]):
        super().__init__()
        self.__config = config
        self.__container = Horizontal()
        self.__maze_generator = MazeGenerator(config)
        self.__canvas = MyCanvas(config.nb_row, config.nb_col, colours=colours)
        self.__maze_generator = MazeGenerator(config)
        self.__generator = self.__maze_generator.generate(animate=True)

    def compose(self) -> ComposeResult:
        # with self.__container:
        yield self.__canvas

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours):
        # TODO: Recreate a Canvas !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # self.__canvas.remove()
        self.__canvas.up_colours(colours)
        # self.__canvas = MyCanvas(200, 200, colours)
        # self.mount(self.__canvas)

    # ########################################################################
    # ######################################################### UP CANVAS ####
    def update_config(self):
        # TODO: Recreate a Canvas !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pass

    # ########################################################################
    # ##################################################### GENERATE MAZE ####
    def generate_new_maze(self):
        self.__generator = self.__maze_generator.generate(animate=True)
        self.__canvas.clear()
        self.next_step_animation()

    def next_step_animation(self) -> bool:
        maze = next(self.__generator, None)
        if maze:
            self.__canvas.dig_holes(maze)
            self.__canvas.refresh()
            return True
        else:
            return False
