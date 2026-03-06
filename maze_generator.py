from typing import List, Tuple, Optional
from Maze import Maze
import random
import time


class MazeGenerator:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.full_path: List[List[Tuple[int, int]]] = []
        self.full_path_flat: Set[Tuple[int, int]] = set()
        self.not_visited = {}

    class Path:
        """
        - Simple class that stores path related info
        - Allows to access actual path (list of coordinates) via index
        """

        def __init__(
            self,
            first: bool,
            path_start: Optional[List[Tuple[int, int]]] = [],
        ) -> None:
            self.first = first
            self.values: List[int] = []
            self.path: List[Tuple[int, int]] = path_start

        def __getitem__(self, index) -> Tuple[int, int]:
            return self.path[index]

        def __len__(self) -> int:
            return len(self.path)

        def append(self, coor: Tuple[int, int]) -> None:
            self.path.append(coor)

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
            full_path: List[List[Tuple[int, int]]],
            first_path: Optional[bool] = False,
        ) -> None:
            """
            - Initalizes path (list of coordinates visited after LERW
                    from a to b) to given start coordinates
            - Stores goal coordinates and outer limits
            """

            self.path = MazeGenerator.Path(first_path, [begin])
            self.end = end
            self.max_r, self.max_c = limits
            self.cur_r, self.cur_c = self.path[-1]
            self.values = values
            self.full_path = set(full_path)
            self.first_path = first_path

        def walk(self) -> List[Tuple[int, int]]:
            """
            - Choose randomly a move possible from last path entry
            - Check for loop/blocked
            - Erase loop if so
            - Else append move to path
            """
            cond = (
                (lambda a, b: a != b)
                if self.first_path
                else (lambda a, b: a not in b)
            )
            while cond(
                (self.cur_r, self.cur_c),
                self.end
                if self.first_path
                else self.full_path,
            ):
                valid_moves = self.__get_valid_moves()
                if len(valid_moves) == 0:
                    self.path = self.path[: int(len(self.path) / 2)]
                else:
                    r, c = random.choice(valid_moves)
                    target = (self.cur_r + r, self.cur_c + c)
                    if target in self.path:
                        self.__go_back(target)
                    else:
                        self.path.append(target)
                self.cur_r, self.cur_c = self.path[-1]
            return self.path

        def __go_back(self, coor: Tuple[int, int]) -> None:
            """
            - Called when loop found by walk()
            - Finds first neighbouring in-path cell
            - Reverts path to index of found cell
            """
            index = min([k for k, v in enumerate(self.path) if v == coor])
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
                    and (
                        len(self.path) == 1 or (new_r, new_c) != self.path[-2]
                    )
                ):
                    valid_moves.append((r, c))
            return valid_moves

    class Translator:
        def __init__(self) -> None:
            pass

        @staticmethod
        def __get_cell_value(
            path: "MazeGenerator.Path", i: int, r: int, c: int
        ) -> int:
            value = 0xF
            wall_map = {
                (-1, 0): 1,  # North
                (1, 0): 4,  # South
                (0, -1): 8,  # West
                (0, 1): 2,  # East
            }
            neighbours = set()
            if i > 0:
                neighbours.add(path[i - 1])
            if i < len(path) - 1:
                neighbours.add(path[i + 1])

            for ngbr_r, ngbr_c in neighbours:
                offset = (ngbr_r - r, ngbr_c - c)
                value -= wall_map.get(offset, 0)
            return value

        @staticmethod
        def translate_and_write_path(
            maze: Maze, path: "MazeGenerator.Path"
        ) -> None:
            for i, (r, c) in enumerate(path):
                maze.values[r][c] = MazeGenerator.Translator.__get_cell_value(
                    path, i, r, c
                )

    def generate(self) -> None:
        walker = self.Walker(
            self.maze.start,
            self.maze.end,
            (self.maze.nb_row, self.maze.nb_col),
            self.maze.values,
            self.full_path_flat,
            True,
        )
        self.not_visited = {(r, c) for r in range(self.maze.nb_row) for c in range(self.maze.nb_col)}
        self.full_path.append(walker.walk())
        for i in self.full_path[-1]:
            self.full_path_flat.add(i)
            self.not_visited.discard(i)
        self.Translator.translate_and_write_path(self.maze, self.full_path[-1])
        self.print_maze()

        while len(self.not_visited) != 0:
            walker = self.Walker(
                random.choice(list(self.not_visited)),
                None,
                (self.maze.nb_row, self.maze.nb_col),
                self.maze.values,
                self.full_path_flat,
                False,
            )
            self.full_path.append(walker.walk()[:-1])
            for i in self.full_path[-1]:
                self.full_path_flat.add(i)
                self.not_visited.discard(i)
            self.Translator.translate_and_write_path(
                self.maze, self.full_path[-1]
            )
            self.print_maze()

    def print_maze(self) -> None:
        for line in self.maze.values:
            for char in line:
                print(f"{char:x}" if char != 0xF else "_", end="")
            print()

        print()
        print()
