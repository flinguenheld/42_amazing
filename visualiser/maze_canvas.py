from copy import deepcopy
from mazegen.maze import Maze
from textual.color import Color
from textual_canvas import Canvas
from typing import Dict, override, Any


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░░█▀▀░█▀█░█▀█░█░█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░░█░░░█▀█░█░█░▀▄▀░█▀█░▀▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░░▀░░▀░▀░▀▀▀
class MazeCanvas(Canvas):
    def __init__(self, nb_row: int, nb_col: int, colours: Dict[str, Color]):
        super().__init__(
            width=(nb_col * 3 + (nb_col + 1)),
            height=(nb_row * 3 + (nb_row + 1)),
            # Background is managed in the css
            # canvas_color=colours["background"],
            # canvas_color=colours["secondary"],
        )
        self._previous_maze: None | Maze = None
        self._colours = colours

        # Keep the size to easily compare with config in TMaze
        self.config_size = (nb_row, nb_col)

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours: Dict[str, Color]) -> None:
        """Save colours and redraw the maze"""
        self._colours = colours
        if self._previous_maze:
            last_maze = deepcopy(self._previous_maze)
            self.clear()
            self.dig_holes(last_maze)

    # ########################################################################
    # ############################################################## DRAW ####
    def _draw_line(
        self,
        row: int,
        col: int,
        vertical: bool = False,
        colour: str = "primary",
    ) -> None:
        if vertical:
            self.draw_line(col, row, col, row + 2, color=self._colours[colour])
        else:
            self.draw_line(col, row, col + 2, row, color=self._colours[colour])

    def _draw_square(
        self, row: int, col: int, colour: str = "primary"
    ) -> None:
        self._draw_line(row - 1, col - 1, False, colour)
        self._draw_line(row, col - 1, False, colour)
        self._draw_line(row + 1, col - 1, False, colour)

    # ########################################################################
    # ######################################################### DRAW HEXA ####
    def draw_line_hexa(
        self,
        row_from: int,
        col_from: int,
        row_to: int,
        col_to: int,
        colour: str,
    ) -> None:
        self.draw_line(
            row_from * 4 + 2,
            col_from * 4 + 2,
            row_to * 4 + 2,
            col_to * 4 + 2,
            self._colours[colour],
        )

    def draw_square_hexa_coordinates(
        self, row: int, col: int, colour: str
    ) -> None:
        self._draw_square(row=row * 4 + 2, col=col * 4 + 2, colour=colour)

    # ########################################################################
    # ############################################################# CLEAR ####
    @override
    def clear(
        self,
        color: Color | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> Any:
        self._previous_maze = None
        return super().clear(color, width, height)

    # ########################################################################
    # ######################################################### DIG HOLES ####
    def dig_holes(self, maze_hexa: Maze) -> None:
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

                # Only draw the updated values --
                if (
                    self._previous_maze
                    and cell_hexa == self._previous_maze.values[rh][ch]
                ):
                    continue

                if cell_hexa & 0b1111 != 0b1111:
                    self._draw_square(row, col)

                if cell_hexa & 0b0001 != 0b0001:  # Top
                    self._draw_line(row - 2, col - 1)
                if cell_hexa & 0b0100 != 0b0100:  # Bottom
                    self._draw_line(row + 2, col - 1)
                if cell_hexa & 0b1000 != 0b1000:  # Left
                    self._draw_line(row - 1, col - 2, vertical=True)
                if cell_hexa & 0b0010 != 0b0010:  # Right
                    self._draw_line(row - 1, col + 2, vertical=True)

        self._previous_maze = deepcopy(maze_hexa)
