from typing import List
from textual.containers import VerticalGroup, HorizontalGroup, Center
from textual.widgets import Static
from textual.app import ComposeResult
from visualiser.tcell import (
    TCell,
    TCellAngle,
    TCellHorizontal,
    TCellVertical,
    TCellMiddle,
)
from maze_generator.maze import Maze
from visualiser.borders import Borders

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
    def __init__(self, maze: Maze, borders: Borders) -> None:
        """
        Create the grid of cells
        """

        super().__init__()
        self.__hexa_maze = maze
        self.__borders = borders
        self.__nb_row = self.__hexa_maze.nb_row * 2 + 1
        self.__nb_col = self.__hexa_maze.nb_col * 2 + 1
        self.__cells = self.__init_cells()

    # ######################################################## INIT CELLS ####
    def __init_cells(self) -> List[List[TCell]]:
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

    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with VerticalGroup():
            for row in self.__cells:
                with HorizontalGroup(classes="col_layout"):
                    for col in row:
                        yield col

    # ##################################################### REFRESH CELLS ####
    def refresh_cells(self) -> None:
        for row in self.__cells:
            for cell in row:
                cell.refresh_cell()

    # #################################################### UP CELLS STATE ####
    def update_cells_state(self) -> None:
        """
        Loop in all hexa cells
        And update all neighbours according to its value
        """
        for rh, row_hexa in enumerate(self.__hexa_maze.values):
            for ch, cell_hexa in enumerate(row_hexa):
                # Get the top left coordinate in self.cells
                row = rh * 2
                col = ch * 2

                #                                                     Top Left
                self.__cells[row][col].up_state(
                    bottom=cell_hexa & 0b1000 == 0b1000,
                    right=cell_hexa & 0b0001 == 0b0001,
                )
                #                                                          Top
                self.__cells[row][col + 1].up_state(
                    active=cell_hexa & 0b0001 == 0b0001
                )
                #                                                    Top Right
                self.__cells[row][col + 2].up_state(
                    left=cell_hexa & 0b0001 == 0b0001,
                    bottom=cell_hexa & 0b0010 == 0b0010,
                )
                #                                                        Right
                self.__cells[row + 1][col + 2].up_state(
                    active=cell_hexa & 0b0010 == 0b0010
                )
                #                                                 Bottom Right
                self.__cells[row + 2][col + 2].up_state(
                    left=cell_hexa & 0b0100 == 0b0100,
                    top=cell_hexa & 0b0010 == 0b0010,
                )
                #                                                       Bottom
                self.__cells[row + 2][col + 1].up_state(
                    active=cell_hexa & 0b0100 == 0b0100
                )
                #                                                  Bottom Left
                self.__cells[row + 2][col].up_state(
                    top=cell_hexa & 0b1000 == 0b1000,
                    right=cell_hexa & 0b0100 == 0b0100,
                )
                #                                                         Left
                self.__cells[row + 1][col].up_state(
                    active=cell_hexa & 0b1000 == 0b1000
                )
                #                                                       Middle
                self.__cells[row + 1][col + 1].up_state(value=cell_hexa)
