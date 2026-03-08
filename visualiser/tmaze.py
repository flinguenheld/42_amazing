from typing import Tuple, List
from textual.containers import VerticalGroup, HorizontalGroup
from textual.widgets import Static
from textual.app import App, ComposeResult, RenderResult
from visualiser.tcell import (
    TCell,
    TCellAngle,
    TCellHorizontal,
    TCellVertical,
    TCellMiddle,
)
from maze import Maze


class TMaze(Static):
    # CSS_PATH = "style/cell.tcss"
    def __init__(self, maze: Maze) -> None:
        """
        Create a grid of cells
        """

        super().__init__()
        self.__hexa_maze = maze
        self.__nb_row = self.__hexa_maze.nb_row * 2 + 1
        self.__nb_col = self.__hexa_maze.nb_col * 2 + 1
        self.__cells = self.__init_maze()

        # self.update_cells()

    # ########################################################## INIT MAZE ####
    def __init_maze(self) -> List[List[TCell]]:

        new_maze = []
        for row in range(0, self.__nb_row):
            new_maze.append([])
            for col in range(0, self.__nb_col):
                match (row % 2 == 0, col % 2 == 0):
                    case (True, True):
                        new_maze[row].append(TCellAngle())
                    case (True, False):
                        new_maze[row].append(TCellHorizontal())
                    case (False, True):
                        new_maze[row].append(TCellVertical())
                    case (False, False):
                        new_maze[row].append(TCellMiddle())
        return new_maze

    # ############################################################ COMPOSE ####
    def compose(self) -> ComposeResult:
        with VerticalGroup(id="maze_layout"):
            for row in self.__cells:
                with HorizontalGroup():
                    for col in row:
                        yield col

    # ########################################################### UP CELLS ####
    def update_cells(self) -> None:

        print("Update cells with:")
        print(self.__hexa_maze)

        # Loop in all hexa cells
        for rh, row_hexa in enumerate(self.__hexa_maze.values):
            for ch, cell_hexa in enumerate(row_hexa):
                # And update neighbours according to its value

                # Get the top left coordinate in self.cells
                row = rh * 2
                col = ch * 2

                print(
                    f"deal with this value: {cell_hexa:x} -> {cell_hexa:04b}"
                )

                #                                                    North West
                self.__cells[row][col].up_value(cell_hexa & 0b1001)
                #                                                         North
                self.__cells[row][col + 1].up_value(
                    cell_hexa & 0b0001 == 0b0001
                )
                #                                                    North East
                self.__cells[row][col + 2].up_value(cell_hexa & 0b0011)
                #                                                          East
                self.__cells[row + 1][col + 2].up_value(
                    cell_hexa & 0b0010 == 0b0010
                )
                #                                                    South East
                self.__cells[row + 2][col + 2].up_value(cell_hexa & 0b0110)
                #                                                         South
                self.__cells[row + 2][col + 1].up_value(
                    cell_hexa & 0b0100 == 0b0100
                )
                #                                                    South West
                self.__cells[row + 2][col].up_value(cell_hexa & 0b1100)
                #                                                          West
                self.__cells[row + 1][col].up_value(
                    cell_hexa & 0b1000 == 0b1000
                )
                #                                                        Middle
                self.__cells[row + 1][col + 1].up_value(cell_hexa)
