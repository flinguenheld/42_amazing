import asyncio
from typing import Dict, Optional
from textual.color import Color
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Horizontal

from mazegen.maze import Maze
from mazegen.config import Config
from visualiser.player import Player
from visualiser.maze_canvas import MazeCanvas
from visualiser.tmessage import TMessageSuccess, TMessageError
from mazegen.maze_generator import MazeGenerator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀
class TMaze(Widget):
    def __init__(self, config: Config, colours: Dict[str, Color]):
        super().__init__()
        self.__config = config
        self.__colours = colours
        self.__container = Horizontal()
        self.__maze_generator = MazeGenerator(config)
        self.__maze_gen_iterator = MazeGenIterator(self.__maze_generator)
        self.__canvas = MazeCanvas(config.nb_row, config.nb_col, colours)
        self.__last_size = (config.nb_row, config.nb_col)
        self.__player: Optional[Player] = None

    def compose(self) -> ComposeResult:
        yield self.__canvas

    # ########################################################################
    # ################################################## PLAYER MOVEMENTS ####
    def move_player(self, key: str):
        if self.__player:
            self.__player.move(key)

            # Clean previous --
            (row, col) = self.__player.get_previous_position()
            self.__canvas.draw_point_hexa_coordinates(row, col, "primary")

            # Victory ? --
            if self.__player.is_winning():
                counter, shortest = self.__player.get_counter()
                self.app.push_screen(
                    TMessageSuccess(
                        f"Done in {counter} steps\n"
                        f"Shortest path: {shortest - 1}"
                    )
                )
                self.reset_player()

            # draw new position --
            else:
                (row, col) = self.__player.get_position()
                self.__canvas.draw_point_hexa_coordinates(row, col, "warning")

    def reset_player(self) -> None:
        if self.__player:
            self.__player.reset()
            self.__canvas.draw_start_exit()

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
        self.__canvas.draw_start_exit()
        self.__player = Player(maze)

    # ########################################################################
    # ######################################################### ANIMATION ####
    def start_new_maze(self):
        """
        Generate a new maze and get an iterator to the first step
        """
        self.__maze_gen_iterator.start_new_generator()
        self.__clear_or_reset_canvas()
        self.next_step_animation()

    async def animate_all_steps(self):
        while self.next_step_animation():
            await asyncio.sleep(0)

    def next_step_animation(self) -> bool:
        maze = self.__maze_gen_iterator.next_step()
        if maze:
            self.__canvas.dig_holes(maze)
            return True
        else:
            # Done !
            self.__canvas.draw_start_exit()
            self.__player = Player(self.__maze_gen_iterator.last_generated())
            return False


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░░█▀▀░█▀▀░█▀█░░░▀█▀░▀█▀░█▀▀░█▀▄░█▀█░▀█▀░█▀█░█▀▄
# ░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░░█░█░█▀▀░█░█░░░░█░░░█░░█▀▀░█▀▄░█▀█░░█░░█░█░█▀▄
# ░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░░▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀
class MazeGenIterator:
    """Wrapper to create a generator and keep the last maze on each step"""

    def __init__(self, generator: MazeGenerator):
        self._last = None
        self._mazegen_iter = None
        self._maze_generator = generator

    def start_new_generator(self) -> None:
        self._last = None
        self._mazegen_iter = self._maze_generator.generate()

    def last_generated(self) -> Optional[Maze]:
        return self._last

    def next_step(self) -> Optional[Maze]:
        if self._mazegen_iter:
            new_maze = next(self._mazegen_iter, None)
            if new_maze:
                self._last = new_maze
                return new_maze

        return None
