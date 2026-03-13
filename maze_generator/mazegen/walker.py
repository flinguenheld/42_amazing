from mazegen.maze import Maze
from mazegen.path import Path
from typing import List, Tuple, Set
import random


class Walker:
    """
    - Class that walks (LERW) from point a to point b in maze
                                                creating a path
    """

    def __init__(
        self,
        maze: Maze,
        __first_path: bool,
        start: Tuple[int, int],
        __end: Set[Tuple[int, int]] | Tuple[int, int],
    ) -> None:

        self.__maze = maze
        self.__path = Path([start])
        self.__first_path = __first_path
        self.__end = {__end} if isinstance(__end, tuple) else __end
        self.__cur_r, self.__cur_c = self.__path[-1]

    def walk(self, rand: random.Random) -> List[Tuple[int, int]]:
        """
        - Randomly choose a possible move from last path entry
        - Check for loop/blocked
        - Erase loop if so
        - Else append move to path
        - Write corresponding values into maze
        - Return Path object
        """
        while (self.__cur_r, self.__cur_c) not in self.__end:
            valid_moves = self.__get_valid_moves()
            if len(valid_moves) == 0:
                return self.__path
            else:
                r, c = rand.choice(self.__get_valid_moves())
                target = (self.__cur_r + r, self.__cur_c + c)
                if target in self.__path:
                    self.__path.go_back(target)
                else:
                    self.__path.append(target)
                self.__cur_r, self.__cur_c = self.__path[-1]
        self.__write_path()
        return self.__path

    def __write_path(self) -> None:
        """
        - Write path data to maze
        """
        for i, cell in enumerate(self.__path):
            if i < len(self.__path) - 1:
                self.__maze.break_wall(
                    self.__path[i], self.__path[i + 1], False
                )

    def __get_valid_moves(
        self,
    ) -> List[Tuple[int, int]]:
        """
        - Try every move and check result is within bounds
        - Return validated moves
        """
        moves = ((0, 1), (0, -1), (1, 0), (-1, 0))
        valid_moves: List[Tuple[int, int]] = []
        for r, c in moves:
            new_r, new_c = (self.__cur_r + r, self.__cur_c + c)
            if (
                0 <= new_r < self.__maze.nb_row
                and 0 <= new_c < self.__maze.nb_col
                and (
                    len(self.__path) == 1 or (new_r, new_c) != self.__path[-2]
                )
                and (new_r, new_c) not in self.__maze.cells_42
            ):
                valid_moves.append((r, c))
        return valid_moves
