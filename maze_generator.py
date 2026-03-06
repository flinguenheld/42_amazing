from typing import List, Tuple
from Maze import Maze
import random
import time


class MazeGenerator:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    class Walker:
        """
        - Class that walks from point a to point b in maze creating a path
        """

        def __init__(
            self,
            begin: Tuple[int, int],
            end: Tuple[int, int],
            limits: Tuple[int, int],
            values: List[List[int]],
        ) -> None:
            """
            - Initalizes path (list of coordinates visited after LERW
                    from a to b) to given start coordinates
            - Stores goal coordinates and outer limits
            """
            self.path = [begin]
            self.end = end
            self.max_r, self.max_c = limits
            self.cur_r, self.cur_c = self.path[-1]
            self.values = values

        def walk(self) -> List[Tuple[int, int]]:
            """
            - Choose randomly a move possible from last path entry
            - Check for loop/blocked
            - Erase loop if so
            - Else append move to path
            """
            while (self.cur_r, self.cur_c) != self.end:
                valid_moves = self.__get_valid_moves()
                if len(valid_moves) == 0:
                    self.path = self.path[:int(len(self.path) / 2)]
                else:
                    r, c = random.choice(valid_moves)
                    target = (self.cur_r + r, self.cur_c + c)
                    if target in self.path:
                        self.__go_back(target)
                    else:
                        self.path.append(target)
                self.cur_r, self.cur_c = self.path[-1]
                self.__update_maze()
            return self.path

        def __go_back(self, coor: Tuple[int, int]) -> None:
            """
            - Called when loop found by walk()
            - Finds first neighbouring in-path cell
            - Reverts path to index of found cell
            """
            try:
                index = min([k for k, v in enumerate(self.path) if v == coor])
            except IndexError:
                index = int(len(self.path) / 2)
            if index < 2:
                index = 2
            self.path = self.path[:index]

        def __get_valid_moves(
            self,
        ) -> List[Tuple[int, int]]:
            """
            - Try every move and check result is within bounds,
                    Not 42, and respect passed lambda condition
            - Return all moves which pass three
            """

            moves = ((0, 1), (0, -1), (1, 0), (-1, 0))
            valid_moves: List[Tuple[int, int]] = []
            for r, c in moves:
                new_r, new_c = (self.cur_r + r, self.cur_c + c)
                if (
                    0 <= new_r < self.max_r
                    and 0 <= new_c < self.max_c
                    and (len(self.path) == 1
                         or (new_r, new_c) != self.path[-2])
                ):
                    valid_moves.append((r, c))
            return valid_moves

        def __update_maze(self) -> None:
            """
            - Writes data from self.path to self.maze.values

            """
            tab = [[0 for k in range(self.max_c)] for r in range(self.max_r)]
            for r, c in self.path:
                tab[r][c] = 1

            for line in tab:
                for char in line:
                    print(char, end="")
                print()

            time.sleep(0.01)
            print()
            print()

#   def __get_cell_value(self, i: int, r: int, c: int) -> int:
#       """
#       - Look at preceding cell
#       - Remove appropriate wall
#       - Look at next cell
#       - Remove appropriate wall
#       """
#       value = 0xF

#       if i > 0 + 1:
#           if self.path[i - 1] == (r - 1, c):
#               value -= 1
#           elif self.path[i - 1] == (r + 1, c):
#               value -= 4
#           elif self.path[i - 1] == (r, c - 1):
#               value -= 8
#           elif self.path[i - 1] == (r, c + 1):
#               value -= 2

#       if i < len(self.path) - 1:
#           if self.path[i + 1] == (r - 1, c):
#               value -= 1
#           elif self.path[i + 1] == (r + 1, c):
#               value -= 4
#           elif self.path[i + 1] == (r, c - 1):
#               value -= 8
#           elif self.path[i + 1] == (r, c + 1):
#               value -= 2

#       return value

#   def __update_maze(self) -> None:
#       """
#       - Writes data from self.path to self.maze.values
#       """
#       print(self.path)
#       for i, (r, c) in enumerate(self.path):
#           self.maze.values[r][c] = self.__get_cell_value(i, r, c)

#       print(self.maze)

    def generate(self) -> None:
        walker = self.Walker(
            self.maze.start,
            self.maze.end,
            (self.maze.nb_row, self.maze.nb_col),
            self.maze.values,
        )
        self.path = walker.walk()
