from textual.reactive import reactive
from typing import List
from textual.widgets import Static
from textual.app import RenderResult
from visualiser.tcell import (
    TCell,
    TCellAngle,
    TCellHorizontal,
    TCellVertical,
    TCellMiddle,
)
from maze_generator.maze import Maze
from visualiser.borders import Borders

from visualiser.mcell import MCellHorizontal, MCellVertical, MCellAngle

# General explanations :
#
# The maze is a List[List[int]]
# Each maze's cell contains an int which represents the walls around itself.
#
# The first four bits are used as well:
#
#   LEFT   BOTTOM   RIGHT   TOP
#    0       1       1       0
#
# This cell with the value 0x6 looks like that:
#
#             ┏━━━
#             ┃
#
# --
# Since we are in a terminal, we have to draw each cell with
# a (or several) characters.
# To do so, we create a new list named "cells" which contains all borders and
# maze's cells.
# Here for one maze's cell:
# ┏━━━━┳━━━━━━━━┳━━━━┓
# ┃ TL ┃  TOP   ┃ TR ┃
# ┣━━━━╋━━━━━━━━╋━━━━┫
# ┃ L  ┃  Cell  ┃ R  ┃
# ┣━━━━╋━━━━━━━━╋━━━━┫
# ┃ BL ┃  BOT   ┃ BR ┃
# ┗━━━━┻━━━━━━━━┻━━━━┛
#
# Here for three:
# ┏━━━━┳━━━━━━━━┳━━━━┳━━━━━━━━┳━━━━┳━━━━━━━━┳━━━━┓
# ┃    ┃        ┃    ┃        ┃    ┃        ┃    ┃
# ┣━━━━╋━━━━━━━━╋━━━━╋━━━━━━━━╋━━━━╋━━━━━━━━╋━━━━┫
# ┃    ┃  HEXA  ┃    ┃  HEXA  ┃    ┃  HEXA  ┃    ┃
# ┣━━━━╋━━━━━━━━╋━━━━╋━━━━━━━━╋━━━━╋━━━━━━━━╋━━━━┫
# ┃    ┃        ┃    ┃        ┃    ┃        ┃    ┃
# ┗━━━━┻━━━━━━━━┻━━━━┻━━━━━━━━┻━━━━┻━━━━━━━━┻━━━━┛
#
# Each cell of this list is a widget based on TCell
# The purpose of TMaze is to update the values of these cell to tell
# them if they have to display a wall and for the angles, to connect with
# their neighbours or not.
#
# Once done, Textual will automaticaly render them.


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀
class TMaze(Static):
    __to_print = reactive("")

    def __init__(self, maze: Maze, borders: Borders) -> None:
        """
        Create the grid of cells
        """

        super().__init__()
        self.__hexa_maze = maze
        self.__borders = borders
        self.__nb_row = self.__hexa_maze.nb_row * 2 + 1
        self.__nb_col = self.__hexa_maze.nb_col * 2 + 1
        self.__cells_TO_REMOVE = self.__init_cells_TO_REMOVE()
        self.refresh_maze_TO_REMOVE()

        self.__cell_angles = MCellAngle(borders)
        self.__cell_verticals = MCellVertical(borders)
        self.__cell_horizontals = MCellHorizontal(borders)

    # ##############
    # def new_maze(self, maze: List[List[int]]) -> None:
    def new_maze(self) -> None:

        for rh, row_hexa in enumerate(self.__hexa_maze.values):
            for ch, cell_hexa in enumerate(row_hexa):
                # Who is active ?
                top = cell_hexa & 0b0001 == 0b0001
                left = cell_hexa & 0b1000 == 0b1000
                right = cell_hexa & 0b0010 == 0b0010
                bottom = cell_hexa & 0b0100 == 0b0100

                # Get the top left coordinate in self.cells
                row = rh * 2
                col = ch * 2

                # ################################################### Top Left
                self.__cell_angles.up(row=row, col=col, bottom=left, right=top)

                # ######################################################## Top
                if top:
                    self.__cell_horizontals.add(row=row, col=col + 1)

                # ################################################## Top Right
                self.__cell_angles.up(
                    row=row,
                    col=col + 2,
                    left=top,
                    bottom=right,
                )

                # ###################################################### Right
                if right:
                    self.__cell_verticals.add(row=row + 1, col=col + 2)

                # ############################################### Bottom Right
                self.__cell_angles.up(
                    row=row + 2,
                    col=col + 2,
                    left=bottom,
                    top=right,
                )

                # ##################################################### Bottom
                if bottom:
                    self.__cell_horizontals.add(row=row + 2, col=col + 1)

                # ################################################ Bottom Left
                self.__cell_angles.up(
                    row=row + 2,
                    col=col,
                    right=bottom,
                    top=left,
                )

                # ####################################################### Left
                if left:
                    self.__cell_verticals.add(row=row + 1, col=col)

    def refresh_maze(self) -> None:

        self.__to_print = ""
        for row in range(0, self.__nb_row):
            self.__to_print += "\n"
            for col in range(0, self.__nb_col):
                match (row % 2 == 0, col % 2 == 0):
                    case (True, True):
                        # new_maze[row].append(TCellAngle(self.__borders))
                        self.__to_print += self.__cell_angles.to_str(row, col)

                    case (True, False):
                        # new_maze[row].append(TCellHorizontal(self.__borders))
                        self.__to_print += self.__cell_horizontals.to_str(
                            row, col
                        )
                    case (False, True):
                        # new_maze[row].append(TCellVertical(self.__borders))
                        self.__to_print += self.__cell_verticals.to_str(
                            row, col
                        )
                    case (False, False):
                        # new_maze[row].append(TCellMiddle(self.__borders))
                        # TODO: TO CHANGE ##################################
                        self.__to_print += "   "

    # ######################################################## INIT CELLS ####
    def __init_cells_TO_REMOVE(self) -> List[List[TCell]]:
        """
        ┏━━━━━━━┳━━━━━━━━┳━━━━━━━┓
        ┃ ANGLE ┃ HORIZO ┃ ANGLE ┃
        ┣━━━━━━━╋━━━━━━━━╋━━━━━━━┫
        ┃ VERTI ┃ MIDDLE ┃ VERTI ┃
        ┣━━━━━━━╋━━━━━━━━╋━━━━━━━┫
        ┃ ANGLE ┃ HORIZO ┃ ANGLE ┃
        ┗━━━━━━━┻━━━━━━━━┻━━━━━━━┛
        """

        new_maze = []
        for row in range(0, self.__nb_row):
            new_maze.append([])
            for col in range(0, self.__nb_col):
                match (row % 2 == 0, col % 2 == 0):
                    case (True, True):
                        new_maze[row].append(TCellAngle(self.__borders))
                    case (True, False):
                        new_maze[row].append(TCellHorizontal(self.__borders))
                    case (False, True):
                        new_maze[row].append(TCellVertical(self.__borders))
                    case (False, False):
                        new_maze[row].append(TCellMiddle(self.__borders))
        return new_maze

    # ############################################################ RENDER ####
    def render(self) -> RenderResult:
        return self.__to_print

    # ###################################################### REFRESH MAZE ####
    def refresh_maze_TO_REMOVE(self) -> None:
        self.__to_print = ""
        for row in self.__cells_TO_REMOVE:
            self.__to_print += "".join(str(cell) for cell in row) + "\n"

    # ##################################################### REFRESH CELLS ####
    def refresh_cells(self) -> None:
        for row in self.__cells_TO_REMOVE:
            for cell in row:
                cell.refresh_cell()
        self.refresh_maze_TO_REMOVE()

    # #################################################### UP CELLS STATE ####
    def update_cells_state(self) -> None:
        """
        Loop in all hexa cells
        And update all neighbours according to its value
        """
        for rh, row_hexa in enumerate(self.__hexa_maze.values):
            for ch, cell_hexa in enumerate(row_hexa):
                # Who is active ?
                top = cell_hexa & 0b0001 == 0b0001
                left = cell_hexa & 0b1000 == 0b1000
                right = cell_hexa & 0b0010 == 0b0010
                bottom = cell_hexa & 0b0100 == 0b0100

                # Get the top left coordinate in self.cells
                row = rh * 2
                col = ch * 2

                # ################################################### Top Left
                self.__cells_TO_REMOVE[row][col].up_state(
                    bottom=left,
                    right=top,
                )

                # ######################################################## Top
                self.__cells_TO_REMOVE[row][col + 1].up_state(active=top)

                # ################################################## Top Right
                self.__cells_TO_REMOVE[row][col + 2].up_state(
                    left=top,
                    bottom=right,
                )

                # ###################################################### Right
                self.__cells_TO_REMOVE[row + 1][col + 2].up_state(active=right)

                # ############################################### Bottom Right
                self.__cells_TO_REMOVE[row + 2][col + 2].up_state(
                    left=bottom,
                    top=right,
                )

                # ##################################################### Bottom
                self.__cells_TO_REMOVE[row + 2][col + 1].up_state(
                    active=bottom
                )

                # ################################################ Bottom Left
                self.__cells_TO_REMOVE[row + 2][col].up_state(
                    right=bottom,
                    top=left,
                )

                # ####################################################### Left
                self.__cells_TO_REMOVE[row + 1][col].up_state(active=left)
