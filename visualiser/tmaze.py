from typing import Dict, Optional, Any

from textual.color import Color
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Horizontal

from mazegen.maze import Maze
from mazegen.config import Config
from mazegen.maze_generator import MazeGenerator
from visualiser.maze_animation import MazeAnimation

from visualiser.player import Player
from visualiser.forty_two import FortyTwo
from visualiser.maze_canvas import MazeCanvas
from visualiser.tmessage import TMessageSuccess


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
        self.__canvas = MazeCanvas(config.nb_row, config.nb_col, colours)
        self.__maze_animation = MazeAnimation(
            self.__maze_generator, self.__canvas.dig_holes
        )
        self.__last_size = (config.nb_row, config.nb_col)

        # Also used to check if maze is ready:
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
        Generate a new maze and place an iterator to the first step
        """
        self.__maze_animation.start_new_animation()
        self.__clear_or_reset_canvas()
        self.__player = None

    def __finish_animation(self):
        if not self.__maze_animation.is_active():
            maze = self.__maze_animation.get_last_maze()
            if maze:
                self.__forty_two.update_points(maze.cells_42)
                self.__player = Player(maze)
                self.__player_draw()
                self.__exit_draw()

    async def animate_all_steps(self) -> None:
        await self.__maze_animation.cycle()
        self.__finish_animation()

    def next_step_animation(self):
        self.__maze_animation.next_step()
        self.__finish_animation()
