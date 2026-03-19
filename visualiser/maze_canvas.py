from copy import deepcopy
from textual.color import Color
from textual_canvas import Canvas
from mazegen.maze import Maze
from typing import Dict, override, Self, Tuple, Any, Generator


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
        self.__previous_maze: None | Maze = None
        self.__colours = colours

    # ########################################################################
    # ########################################################### COLOURS ####
    def up_colours(self, colours: Dict[str, Color]) -> None:
        """Save colours and redraw the maze"""
        self.__colours = colours
        if self.__previous_maze:
            last_maze = deepcopy(self.__previous_maze)
            self.clear()
            self.dig_holes(last_maze)

    # ########################################################################
    # ############################################################## DRAW ####
    def __draw_line(
        self,
        row: int,
        col: int,
        vertical: bool = False,
        colour: str = "primary",
    ) -> None:
        if vertical:
            self.draw_line(
                col, row, col, row + 2, color=self.__colours[colour]
            )
        else:
            self.draw_line(
                col, row, col + 2, row, color=self.__colours[colour]
            )

    def __draw_square(
        self, row: int, col: int, colour: str = "primary"
    ) -> None:
        self.__draw_line(row - 1, col - 1, False, colour)
        self.__draw_line(row, col - 1, False, colour)
        self.__draw_line(row + 1, col - 1, False, colour)

    # ########################################################################
    # ######################################################### DRAW HEXA ####
    def draw_point_hexa_coordinates(
        self, row: int, col: int, colour: str
    ) -> None:
        self.__draw_square(row=row * 4 + 2, col=col * 4 + 2, colour=colour)

    def draw_exit(self) -> None:
        # Use the previous maze to easily call the method with animation

        if self.__previous_maze:
            self.draw_point_hexa_coordinates(
                row=self.__previous_maze.exit[0],
                col=self.__previous_maze.exit[1],
                colour="success",
            )

    # ########################################################################
    # ############################################################# CLEAR ####
    @override
    def clear(
        self,
        color: Color | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> Any:
        self.__previous_maze = None
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
                    self.__previous_maze
                    and cell_hexa == self.__previous_maze.values[rh][ch]
                ):
                    continue

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

        self.__previous_maze = deepcopy(maze_hexa)
