import asyncio
from typing import Dict
from textual.color import Color
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Horizontal
from visualiser.maze_canvas import MazeCanvas
from mazegen.maze_generator import MazeGenerator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀
class TMaze(Widget):
    def __init__(self, config, colours: Dict[str, Color]):
        super().__init__()
        self.__config = config
        self.__colours = colours
        self.__container = Horizontal()
        self.__canvas = MazeCanvas(
            config.nb_row, config.nb_col, colours=colours
        )
        self.__mazegen_iter = None
        self.__maze_generator = MazeGenerator(config)
        self.__last_size = (config.nb_row, config.nb_col)

    def compose(self) -> ComposeResult:
        yield self.__canvas

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours):
        self.__colours = colours
        self.__canvas.up_colours(colours)

    # ########################################################################
    # ###################################################### RESET CANVAS ####
    def reset_canvas(self):
        """
        Delete the current canvas to create and mount a brand new one
        (mandatory to change the area size and adapt the position)
        """
        self.__canvas.remove()
        self.__canvas = MazeCanvas(
            self.__config.nb_row, self.__config.nb_col, colours=self.__colours
        )
        self.mount(self.__canvas)

    # ########################################################################
    # #################################################### CLEAR OR RESET ####
    def __clear_or_reset_canvas(self) -> None:
        """
        Only reset when the size has been updated
        """
        if (self.__config.nb_row, self.__config.nb_col) != self.__last_size:
            self.reset_canvas()
            self.__last_size = (self.__config.nb_row, self.__config.nb_col)
        else:
            self.__canvas.clear()

    # ########################################################################
    # ##################################################### GENERATE MAZE ####
    def generate_new_maze(self):
        """
        Generate a new maze and display it directly
        """
        maze = self.__maze_generator.get_maze()
        self.__clear_or_reset_canvas()
        self.__canvas.dig_holes(maze)

    # ########################################################################
    # ######################################################### ANIMATION ####
    def start_new_maze(self):
        """
        Generate a new maze and get an iterator to the first step
        """
        self.__mazegen_iter = self.__maze_generator.generate()
        self.__clear_or_reset_canvas()
        self.next_step_animation()

    async def animate_all_steps(self):
        while self.next_step_animation():
            await asyncio.sleep(0)

    def next_step_animation(self) -> bool:
        if self.__mazegen_iter:
            maze = next(self.__mazegen_iter, None)
            if maze:
                self.__canvas.dig_holes(maze)
                return True
        return False
