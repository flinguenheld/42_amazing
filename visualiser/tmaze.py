from typing import Dict, Optional, Any

from textual.color import Color
from textual.widget import Widget
from textual.app import ComposeResult

from mazegen.config import Config
from mazegen.maze_generator import MazeGenerator

from visualiser.player import Player
from visualiser.solution import Solution
from visualiser.forty_two import FortyTwo
from visualiser.maze_canvas import MazeCanvas
from visualiser.tmessage import TMessageSuccess
from visualiser.maze_animation import MazeAnimation


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀
class TMaze(Widget):
    def __init__(self, config: Config, colours: Dict[str, Color]):
        super().__init__()
        self._config = config
        self._colours = colours

        self._maze_generator = MazeGenerator(config=config)
        self._canvas = MazeCanvas(config.nb_row, config.nb_col, colours)
        self._maze_animation = MazeAnimation(
            self._maze_generator, self._canvas.dig_holes
        )

        # Use to smartly clear or reset the canvas
        self._last_size = (config.nb_row, config.nb_col)

        self._solution = Solution(self.__solution_draw_cell)
        self._forty_two = FortyTwo(self.__forty_two_draw_cell)

        self._player: Optional[Player] = None
        self._active_maze: Optional[Player] = None

    def compose(self) -> ComposeResult:
        yield self._canvas

    # ########################################################################
    # ################################################## PLAYER MOVEMENTS ####
    def move_player(self, key: str) -> None:
        if self._active_maze and self._player:
            self.player_clean()
            self._player.move(key)
            self._solution.clean_up_to(self._player.get_position())

            # Victory ? --
            if self._player.is_winning():
                counter, shortest = self._player.get_counter()
                self.app.push_screen(
                    TMessageSuccess(
                        f"Done in {counter} steps\n"
                        f"Shortest path: {shortest - 1}"
                    )
                )
                self.player_reset()

            # draw new position --
            else:
                self.__draw_player()

    # ########################################################################
    # ###################################################### PLAYER RESET ####
    def player_reset(self) -> None:
        if self._player:
            self._player.reset()
            self.__draw_player()

    # ########################################################################
    # ####################################################### PLAYER DRAW ####
    def player_clean(self) -> None:
        self.__draw_player(colour="primary")

    def __draw_player(self, colour: str = "warning") -> None:
        if self._player:
            row, col = self._player.get_position()
            self._canvas.draw_square_hexa_coordinates(row, col, colour)

    # ########################################################################
    # ######################################################### EXIT DRAW ####
    def __draw_exit(self) -> None:
        if self._player:
            self._canvas.draw_exit()

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours: Dict[Any, Any]) -> None:
        self._colours = colours
        self._canvas.up_colours(colours)
        self.__draw_player()
        self.__draw_exit()

    # ########################################################################
    # ###################################################### RESET CANVAS ####
    def reset_canvas(self) -> None:
        """
        Delete the current canvas to create and mount a brand new one
        (mandatory to change the area size and adapt the position)
        """
        self._canvas.clear()
        self._canvas.remove()

        self._canvas = MazeCanvas(
            self._config.nb_row, self._config.nb_col, colours=self._colours
        )

        self._maze_animation = MazeAnimation(
            self._maze_generator, self._canvas.dig_holes
        )

        self.mount(self._canvas)

    # ########################################################################
    # #################################################### CLEAR OR RESET ####
    def __clear_or_reset_canvas(self) -> None:
        """
        Only reset when the size has been updated
        """
        if (self._config.nb_row, self._config.nb_col) != self._last_size:
            self.reset_canvas()
            self._last_size = (self._config.nb_row, self._config.nb_col)
        else:
            self._canvas.clear()

    # ########################################################################
    # ################################################################ 42 ####
    async def run_forty_two(self) -> None:
        if self._player:
            await self._forty_two.cycle()

    def __forty_two_draw_cell(self, row, col, colour) -> None:
        """Method called by FortyTwo"""
        self._canvas.draw_square_hexa_coordinates(row, col, colour)

    # ########################################################################
    # ########################################################## SOLUTION ####
    async def run_solution(self) -> None:
        if self._active_maze and self._player:
            self.deactivate_solution()

            await self._solution.cycle(
                self._active_maze, self._player.get_position()
            )

    def deactivate_solution(self) -> None:
        self._solution.deactivate(True)
        self.__draw_exit()
        self.__draw_player()

    def __solution_draw_cell(
        self,
        row_from: int,
        col_from: int,
        row_to: int,
        col_to: int,
        colour: str,
    ):
        """Method called by Solution"""
        self._canvas.draw_line_hexa(row_from, col_from, row_to, col_to, colour)

    # ########################################################################
    # ##################################################### GENERATE MAZE ####
    def generate_new_maze(self) -> None:
        """
        Generate a new maze and display it directly
        """
        self._solution.deactivate(clean=False)

        self._active_maze = self._maze_generator.get_maze()
        self._forty_two.update_points(self._active_maze.cells_42)
        self.__clear_or_reset_canvas()
        self._canvas.dig_holes(self._active_maze)
        self._player = Player(self._active_maze)
        self.__draw_player()
        self.__draw_exit()

    # ########################################################################
    # ######################################################### ANIMATION ####
    def start_new_maze(self) -> None:
        """
        Generate a new maze and place an iterator to the first step
        """
        self._solution.deactivate(clean=False)

        self._maze_animation.start_new_animation()
        self.__clear_or_reset_canvas()
        self._player = None
        self.__maze = None

    def __finish_animation(self):
        if not self._maze_animation.is_active():
            maze = self._maze_animation.get_last_maze()
            if maze:
                self._active_maze = maze
                self._forty_two.update_points(self._active_maze.cells_42)
                self._player = Player(self._active_maze)
                self.__draw_player()
                self.__draw_exit()

    async def animate_all_steps(self) -> None:
        await self._maze_animation.cycle()
        self.__finish_animation()

    def next_step_animation(self):
        self._maze_animation.next_step()
        self.__finish_animation()
