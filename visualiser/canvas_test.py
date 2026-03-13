from maze_generator.maze import Maze
from textual.widget import Widget
from maze_generator.config import Config
from textual.containers import Horizontal
from textual.widgets import Static
from textual.app import App, ComposeResult
from textual_canvas import Canvas

from textual.color import Color
from textual.geometry import Offset

from maze_generator.maze_generator import MazeGenerator


class MyCanvas(Canvas):
    def __init__(self, nb_row: int, nb_col: int):
        super().__init__(
            width=(nb_col * 2 + 1) * 10, height=(nb_row * 2 + 1) * 10
        )

    # ############################################################## DRAW ####
    def __draw_line(self, row: int, col: int, vertical: bool = False):
        if vertical:
            self.draw_line(col, row, col, row + 2)
        else:
            self.draw_line(col, row, col + 2, row)

    def __draw_square(self, row, col):
        self.__draw_line(row - 1, col - 1)
        self.__draw_line(row, col - 1)
        self.__draw_line(row + 1, col - 1)

    # ####################################################### BREAK WALLS ####
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


class CMaze(Static):
    def __init__(self, config):
        super().__init__()
        self.__config = config
        self.__container = Horizontal()
        self.__maze_generator = MazeGenerator(config)
        self.__canvas = MyCanvas(config.nb_row, config.nb_col)
        self.__maze_generator = MazeGenerator(config)
        self.__generator = self.__maze_generator.generate(animate=True)

    def compose(self) -> ComposeResult:
        with self.__container:
            yield self.__canvas

    # ########################################################################
    # ########################################################## NEW MAZE ####
    # def init_canvas(self):
    #     self.__nb_col = self.__config.nb_col * 2 + 1
    #     self.__nb_row = self.__config.nb_row * 2 + 1
    #     if self.__canvas:
    #         self.__container.remove_children([self.__canvas])
    #     self.__canvas = Canvas(self.__nb_col, self.__nb_row)
    #     self.__container.mount(self.__canvas)

    # ########################################################################
    # ######################################################### UP CANVAS ####
    # def up_canvas(self):
    # self.__canvas.set_pixel(10, 0)
    # self.__canvas.break_walls(self._maze)
    # self.__canvas.refresh()

    def update_config(self):
        # Create a new Canvas !!!!!!
        pass

    # ########################################################################
    # ##################################################### GENERATE MAZE ####
    def generate_new_maze(self):
        # if (
        #     self.__config.nb_row * 2 + 1 != self.__nb_row
        #     or self.__config.nb_col * 2 + 1 != self.__nb_col
        # ):
        #     self.init_canvas()
        # else:
        #     self.__canvas.clear()
        self.__generator = self.__maze_generator.generate(animate=True)
        self.__canvas.clear()
        self.next_step_animation()

    def next_step_animation(self) -> bool:
        maze = next(self.__generator, None)
        if maze:
            # self.__hexa_maze = maze
            # self.print_RENAME()
            self.__canvas.dig_holes(maze)
            self.__canvas.refresh()
            return True
        else:
            return False
