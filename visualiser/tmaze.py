from typing import Tuple
from textual.containers import VerticalGroup, HorizontalGroup
from textual.widgets import Static
from textual.app import App, ComposeResult, RenderResult
from visualiser.tcell import TCell
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
        self.cells = [
            [TCell() for _ in range(0, self.__nb_col)]
            for _ in range(0, self.__nb_row)
        ]

    def compose(self) -> ComposeResult:
        with VerticalGroup(id="maze_layout"):
            for row in self.cells:
                with HorizontalGroup():
                    for col in row:
                        yield col

    # def __get_neighbours(self, row: int, col: int):

    #     pass
    def __up_neighbour(self, row: int, col: int, mask: int):
        if row <= self.__nb_row and col <= self.__nb_col:
            self.cells[row][col].value |= mask

    def update_cells(self) -> None:
        # Loop in all hexa cells
        for rh, row_hexa in enumerate(self.__hexa_maze.values):
            for ch, cell_hexa in enumerate(row_hexa):
                # And update neighbours according to its value

                # Get the top left coordinate in self.cells
                row = rh * 2
                col = ch * 2

                #                                                    North West
                self.__up_neighbour(row, col, cell_hexa & 0b1001)
                #                                                         North
                self.__up_neighbour(row, col + 1, cell_hexa & 0b0001)
                #                                                    North East
                self.__up_neighbour(row, col + 2, cell_hexa & 0b0011)
                #                                                          East
                self.__up_neighbour(row, col + 2, cell_hexa & 0b0010)
                #                                                    South East
                self.__up_neighbour(row, col + 2, cell_hexa & 0b0110)
                #                                                         South
                self.__up_neighbour(row, col + 2, cell_hexa & 0b0100)
                #                                                    South West
                self.__up_neighbour(row, col + 2, cell_hexa & 0b1100)
                #                                                          West
                self.__up_neighbour(row, col + 2, cell_hexa & 0b1000)
                #                                                        Middle
                self.__up_neighbour(row, col + 2, cell_hexa & 0b1111)
