from time import sleep
import asyncio
from typing import Dict, Optional, Any
from textual.color import Color
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Horizontal

from mazegen.maze import Maze
from mazegen.config import Config
from mazegen.maze_generator import MazeGenerator

from visualiser.forty_two import FortyTwo
from visualiser.player import Player
from visualiser.maze_canvas import MazeCanvas
from visualiser.tmessage import TMessageSuccess, TMessageError


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

        # Also use to check if maze is ready:
        self.__player: Optional[Player] = None
        self.__forty_two = FortyTwo(self.__forty_two_draw_cell)

    def compose(self) -> ComposeResult:
        yield self.__canvas

    # ########################################################################
    # ################################################## PLAYER MOVEMENTS ####
    def move_player(self, key: str) -> None:
        if self.__player:
            self.player_clean()
            self.__player.move(key)

            # Victory ? --
            if self.__player.is_winning():
                counter, shortest = self.__player.get_counter()
                self.app.push_screen(
                    TMessageSuccess(
                        f"Done in {counter} steps\n"
                        f"Shortest path: {shortest - 1}"
                    )
                )
                self.player_reset()

            # draw new position --
            else:
                self.__player_draw()

    # ########################################################################
    # ###################################################### PLAYER RESET ####
    def player_reset(self) -> None:
        if self.__player:
            self.__player.reset()
            self.__player_draw()

    # ########################################################################
    # ####################################################### PLAYER DRAW ####
    def player_clean(self) -> None:
        self.__player_draw(colour="primary")

    def __player_draw(self, colour: str = "warning") -> None:
        if self.__player:
            row, col = self.__player.get_position()
            self.__canvas.draw_point_hexa_coordinates(row, col, colour)

    # ########################################################################
    # ######################################################### EXIT DRAW ####
    def __exit_draw(self) -> None:
        if self.__player:
            self.__canvas.draw_exit()

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours: Dict[Any, Any]) -> None:
        self.__colours = colours
        self.__canvas.up_colours(colours)
        self.__player_draw()
        self.__exit_draw()

    # ########################################################################
    # ###################################################### RESET CANVAS ####
    def reset_canvas(self) -> None:
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
    # ################################################################ 42 ####
    async def run_forty_two(self) -> None:
        if self.__player:
            await self.__forty_two.cycle()

    def __forty_two_draw_cell(self, row, col, colour):
        """Method called by FortyTwo"""
        self.__canvas.draw_point_hexa_coordinates(row, col, colour)

    # ########################################################################
    # ##################################################### GENERATE MAZE ####
    def generate_new_maze(self) -> None:
        """
        Generate a new maze and display it directly
        """
        maze = self.__maze_generator.get_maze()
        self.__forty_two.update_points(maze.cells_42)
        self.__clear_or_reset_canvas()
        self.__canvas.dig_holes(maze)
        self.__player = Player(maze)
        self.__player_draw()
        self.__exit_draw()

    # ########################################################################
    # ######################################################### ANIMATION ####
    def start_new_maze(self) -> None:
        """
        Generate a new maze and get an iterator to the first step
        """
        self.__player = None
        self.__maze_gen_iterator.start_new_generator()
        self.__clear_or_reset_canvas()
        self.next_step_animation()

    async def animate_all_steps(self) -> None:
        while self.next_step_animation():
            await asyncio.sleep(0)

    def next_step_animation(self) -> bool:
        if self.__maze_gen_iterator.in_progress():
            maze = self.__maze_gen_iterator.next_step()
            if maze:
                self.__canvas.dig_holes(maze)
                return True
            else:
                # Done !
                final_maze = self.__maze_gen_iterator.last_generated()
                if final_maze:
                    self.__player = Player(final_maze)
                    self.__forty_two.update_points(final_maze.cells_42)
                    self.__player_draw()
                    self.__exit_draw()

        return False


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░░█▀▀░█▀▀░█▀█░░░▀█▀░▀█▀░█▀▀░█▀▄░█▀█░▀█▀░█▀█░█▀▄
# ░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░░█░█░█▀▀░█░█░░░░█░░░█░░█▀▀░█▀▄░█▀█░░█░░█░█░█▀▄
# ░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░░▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀
class MazeGenIterator:
    """Wrapper to create a generator and keep the last maze on each step"""

    def __init__(self, generator: MazeGenerator):
        self._last: Optional[Maze] = None
        self._mazegen_iter = None
        self._in_progress = False
        self._maze_generator = generator

    def start_new_generator(self) -> None:
        self._mazegen_iter = self._maze_generator.generate()
        self._in_progress = True
        self._last = None

    def last_generated(self) -> Optional[Maze]:
        return self._last

    def in_progress(self) -> bool:
        return self._in_progress

    def next_step(self) -> Optional[Maze]:
        if self._mazegen_iter and self._in_progress:
            new_maze = next(self._mazegen_iter, None)
            if new_maze:
                self._last = new_maze
                return new_maze
            else:
                self._in_progress = False

        return None
