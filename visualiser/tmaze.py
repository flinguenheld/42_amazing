import asyncio
from typing import Dict, Optional, Any

from textual.color import Color
from textual.widget import Widget
from textual.app import ComposeResult

from mazegen import Maze, Config, MazeGenerator

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

        self._solution = Solution(self._solution_draw_cell)
        self._forty_two = FortyTwo(self.__forty_two_draw_cell)

        self._player: Optional[Player] = None
        self._active_maze: Optional[Maze] = None

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
            if self._player.has_won():
                counter, shortest = self._player.get_counter()
                self.app.push_screen(
                    TMessageSuccess(
                        f"Done in {counter} steps\n"
                        f"Shortest path: {shortest - 1}"
                    )
                )
                self.player_reset()
                self._draw_exit()

            # draw new position --
            else:
                self._draw_player()

    # ########################################################################
    # ###################################################### PLAYER RESET ####
    def player_reset(self) -> None:
        if self._player:
            self._player.reset()
            self._draw_player()

    # ########################################################################
    # ####################################################### PLAYER DRAW ####
    def player_clean(self) -> None:
        self._draw_player(colour="primary")

    def _draw_player(self, colour: str = "warning") -> None:
        if self._player:
            row, col = self._player.get_position()
            self._canvas.draw_square_hexa_coordinates(row, col, colour)

    # ########################################################################
    # ######################################################### EXIT DRAW ####
    def _draw_exit(self) -> None:
        if self._active_maze and self._player:
            self._canvas.draw_square_hexa_coordinates(
                row=self._active_maze.exit[0],
                col=self._active_maze.exit[1],
                colour="success",
            )

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours: Dict[Any, Any]) -> None:
        self._colours = colours
        self._canvas.up_colours(colours)
        self._draw_player()
        self._draw_exit()

    # ########################################################################
    # #################################################### CLEAR OR RESET ####
    def _clear_or_reset_canvas(self) -> None:
        """
        Only reset when the config size has been updated
        """
        if (
            self._config.nb_row,
            self._config.nb_col,
        ) != self._canvas.config_size:
            self.reset_canvas()
        else:
            self._canvas.clear()

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

        # Also recreate a MazeAnimation since the canvas is a new object
        self._maze_animation = MazeAnimation(
            self._maze_generator, self._canvas.dig_holes
        )

        self.mount(self._canvas)

    # ########################################################################
    # ################################################################ 42 ####
    async def forty_two_run(self) -> None:
        if self._active_maze:
            asyncio.create_task(self._forty_two.cycle())

    def __forty_two_draw_cell(self, row: int, col: int, colour: str) -> None:
        """Method called by FortyTwo"""
        self._canvas.draw_square_hexa_coordinates(row, col, colour)

    # ########################################################################
    # ########################################################## SOLUTION ####
    async def solution_run(self) -> None:
        if self._active_maze and self._player:
            self.solution_deactivate()

            await self._solution.cycle(
                self._active_maze, self._player.get_position()
            )

    def solution_deactivate(self) -> None:
        self._solution.deactivate(True)
        self._draw_exit()
        self._draw_player()

    def _solution_draw_cell(
        self,
        row_from: int,
        col_from: int,
        row_to: int,
        col_to: int,
        colour: str,
    ) -> None:
        """Method called by Solution"""
        self._canvas.draw_line_hexa_coordinates(
            row_from, col_from, row_to, col_to, colour
        )

    # ########################################################################
    # ##################################################### GENERATE MAZE ####
    def generate_new_maze(self) -> None:
        """
        Generate a new maze and display it directly
        """
        if self._maze_animation.is_active():
            self._maze_animation.kill_animation()

        self._solution.deactivate(clean=False)
        self._forty_two.deactivate()

        self._active_maze = self._maze_generator.get_maze()
        self._forty_two.update_points(self._active_maze.cells_42)
        self._clear_or_reset_canvas()
        self._canvas.dig_holes(self._active_maze)
        self._player = Player(self._active_maze)
        self._draw_player()
        self._draw_exit()

    # ########################################################################
    # ######################################################### ANIMATION ####
    def start_new_maze(self) -> None:
        """
        Generate a new maze and place an iterator to the first step
        """
        self._solution.deactivate(clean=False)
        self._clear_or_reset_canvas()

        self._maze_animation.start_new_animation()
        self._forty_two.deactivate()
        self._player = None
        self._maze = None

    def _finish_animation(self) -> None:
        if not self._maze_animation.is_active():
            maze = self._maze_animation.get_last_maze()
            if maze:
                self._active_maze = maze
                self._forty_two.update_points(self._active_maze.cells_42)
                self._player = Player(self._active_maze)
                self._draw_player()
                self._draw_exit()

    async def animate_all_steps(self) -> None:
        if await self._maze_animation.cycle():
            self._finish_animation()

    def next_step_animation(self) -> None:
        self._maze_animation.next_step()
        self._finish_animation()

    # ########################################################################
    # ################################################### STOP ANIMATIONS ####
    def stop_animations(self) -> None:
        self._maze_animation.stop_animation()
        self._solution.stop_animation()
