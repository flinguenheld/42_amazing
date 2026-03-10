from maze import Maze
from maze_generator.path import Path
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
        first_path: bool,
        start: Tuple[int, int],
        end: Set[Tuple[int, int]] | int,
    ) -> None:

        self.maze = maze
        self.path = Path([start])
        self.first_path = first_path
        self.end = {end} if isinstance(end, tuple) else end
        self.max_r, self.max_c = maze.nb_row, maze.nb_col
        self.cur_r, self.cur_c = self.path[-1]

    def walk(self) -> List[Tuple[int, int]]:
        """
        - Randomly choose a possible move from last path entry
        - Check for loop/blocked
        - Erase loop if so
        - Else append move to path
        - Write corresponding values into maze
        - Return Path object
        """
        while (self.cur_r, self.cur_c) not in self.end:
            valid_moves = self.__get_valid_moves()
            if len(valid_moves) == 0:
                return self.path
            else:
                r, c = random.choice(self.__get_valid_moves())
                target = (self.cur_r + r, self.cur_c + c)
                if target in self.path:
                    self.path.go_back(target)
                else:
                    self.path.append(target)
                self.cur_r, self.cur_c = self.path[-1]
        self.path.write(self.maze, self.first_path)
        return self.path

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
            new_r, new_c = (self.cur_r + r, self.cur_c + c)
            if (
                0 <= new_r < self.max_r
                and 0 <= new_c < self.max_c
                and (len(self.path) == 1 or (new_r, new_c) != self.path[-2])
            ):
                valid_moves.append((r, c))
        return valid_moves
