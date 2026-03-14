import asyncio
from typing import Dict
from textual.color import Color
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Horizontal
from visualiser.maze_canvas import MazeCanvas
from maze_generator.maze_generator import MazeGenerator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀
class TMaze(Widget):
    def __init__(self, config, colours: Dict[str, Color]):
        super().__init__()
        self.__config = config
        self.__container = Horizontal()
        self.__canvas = MazeCanvas(
            config.nb_row, config.nb_col, colours=colours
        )
        self.__maze_generator = MazeGenerator(config)
        self.__mazegen_iter = None

    def compose(self) -> ComposeResult:
        yield self.__canvas

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours):
        self.__canvas.up_colours(colours)
        # ADD REFRESH ??????????????????????????????????????????????????

    # ########################################################################
    # ######################################################### UP CANVAS ####
    def update_config(self):
        # TODO: Recreate a Canvas !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pass

    # ########################################################################
    # ##################################################### GENERATE MAZE ####
    def generate_new_maze(self):
        self.__mazegen_iter = self.__maze_generator.generate(animate=True)
        self.__canvas.clear()
        self.next_step_animation()

    # ########################################################################
    # ######################################################### ANIMATION ####
    async def animate_all_steps(self):
        while self.next_step_animation():
            await asyncio.sleep(0)

    def next_step_animation(self) -> bool:
        if self.__mazegen_iter:
            maze = next(self.__mazegen_iter, None)
            if maze:
                self.__canvas.dig_holes(maze)
                self.__canvas.refresh()
                return True
        return False
