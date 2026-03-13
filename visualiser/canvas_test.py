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
        super().__init__(width=nb_col * 2 + 1, height=nb_row * 2 + 1)

    def break_walls(self, maze: Maze):
        """
        ┏━━━━┳━━━━━━━━┳━━━━┓
        ┃ TL ┃  TOP   ┃ TR ┃
        ┣━━━━╋━━━━━━━━╋━━━━┫
        ┃ L  ┃  Cell  ┃ R  ┃
        ┣━━━━╋━━━━━━━━╋━━━━┫
        ┃ BL ┃  BOT   ┃ BR ┃
        ┗━━━━┻━━━━━━━━┻━━━━┛
        """

        # Loop in the maze and remove walls
        for rh, row_hexa in enumerate(maze.values):
            for ch, cell_hexa in enumerate(row_hexa):
                # Who is active ?
                top = cell_hexa & 0b0001 == 0b0001
                left = cell_hexa & 0b1000 == 0b1000
                right = cell_hexa & 0b0010 == 0b0010
                bottom = cell_hexa & 0b0100 == 0b0100

                # Get the top left coordinate in self.cells
                row = rh * 2
                col = ch * 2

                if cell_hexa & 0b1111 != 0b1111:
                    self.set_pixel(col + 1, row + 1)

                if not top:
                    self.set_pixel(col + 1, row)
                if not right:
                    self.set_pixel(col + 2, row + 1)
                if not bottom:
                    self.set_pixel(col + 1, row + 2)
                if not left:
                    self.set_pixel(col, row + 1)


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
            self.__canvas.break_walls(maze)
            self.__canvas.refresh()
            return True
        else:
            return False
