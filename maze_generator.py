from typing import List, Tuple, Set, Dict
from Maze import Maze
import random

# TODO: Add '42' to the middle of the maze when possible
# TODO: Write docstrings for all functions
# TODO: Instantiate maze inside MazeGenerator and return it on generate()


class MazeGenerator:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.fp = self.FullPath()
        self.not_visited = {
            (r, c)
            for r in range(self.maze.nb_row)
            for c in range(self.maze.nb_col)
        }
        # random.seed(4)

    class Path:
        """
        - Simple class that stores path related info
        - Allows to access actual path (list of coordinates) via index
        """

        def __init__(
            self,
            path_start: List[Tuple[int, int]],
        ) -> None:
            self.values: Dict[Tuple[int, int],  int] = dict()
            self.path: List[Tuple[int, int]] = path_start
            self.dirs: Dict[str, Tuple[int, int]] = {
                "N": (-1, 0),
                "E": (0, 1),
                "S": (1, 0),
                "W": (0, -1),
            }
            self.wall_map: Dict[Tuple[int, int], int] = {
                self.dirs["N"]: 0b0001,
                self.dirs["E"]: 0b0010,
                self.dirs["S"]: 0b0100,
                self.dirs["W"]: 0b1000,
            }

        def __getitem__(self, index) -> Tuple[int, int]:
            return self.path[index]

        def __len__(self) -> int:
            return len(self.path)

        def append(self, coor: Tuple[int, int]) -> None:
            self.path.append(coor)

        def go_back(self, target: Tuple[int, int]) -> None:
            index = [k for k, v in enumerate(self.path) if v == target][0]
            self.path = self.path[: index + 1]

        def __get_cell_value(self, i: int) -> int:
            value = 0xF
            r, c = self.path[i]
            neighbours = set()
            # breakpoint()
            if i > 0:
                neighbours.add(self.path[i - 1])
            if i < len(self.path) - 1:
                neighbours.add(self.path[i + 1])

            for ngbr_r, ngbr_c in neighbours:
                offset = (ngbr_r - r, ngbr_c - c)
                value = value & ~(self.wall_map.get(offset, 0))
            return value

        def __get_last_value(self, maze: Maze) -> None:
            r, c = self.path[-1]
            prev_r, prev_c = self.path[-2]
            offset = (r - prev_r, c - prev_c)
            maze.values[prev_r][prev_c] = maze.values[prev_r][prev_c] & ~(
                self.wall_map.get(offset, 0)
            )
            offset = (prev_r - r, prev_c - c)
            maze.values[r][c] = maze.values[r][c] & ~(
                self.wall_map.get(offset, 0)
            )

        def write(self, maze: Maze, first_path: bool) -> None:
            for i, (r, c) in enumerate(self.path[:-1]):
                maze.values[r][c] = self.__get_cell_value(i)
            if first_path is False:
                self.__get_last_value(maze)
            else:
                r, c = self.path[-1]
                maze.values[r][c] = self.__get_cell_value(len(self.path) - 1)

    class FullPath:
        """
        - Class that stores both a list of Paths
                    And a flattened set of said list
        """

        def __init__(self) -> None:
            self.full_path: List["MazeGenerator.Path"] = list()
            self.full_path_flat: Set[Tuple[int, int]] = set()

        def __getitem__(self, index) -> "MazeGenerator.Path":
            return self.full_path[index]

        def __len__(self) -> int:
            return len(self.full_path)

        def append(self, path: "MazeGenerator.Path") -> List[Tuple[int, int]]:
            self.full_path.append(path)
            for coor in path:
                self.full_path_flat.add(coor)
            return path

        def get_list(self) -> List["MazeGenerator.Path"]:
            return self.full_path

        def get_set(self) -> Set[Tuple[int, int]]:
            return self.full_path_flat

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
            self.path = MazeGenerator.Path([start])
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
                    and (
                        len(self.path) == 1 or (new_r, new_c) != self.path[-2]
                    )
                ):
                    valid_moves.append((r, c))
            return valid_moves

    def generate(self) -> None:
        walker = self.Walker(self.maze, True, self.maze.start, self.maze.end)
        for coor in self.fp.append(walker.walk()):
            self.not_visited.discard(coor)
        self.print_maze()

        while len(self.not_visited) != 0:
            choice = random.choice(list(self.not_visited))
            walker = self.Walker(self.maze, False, choice, self.fp.get_set())
            for coor in self.fp.append(walker.walk()):
                self.not_visited.discard(coor)

# TESTING RELATED CODE
# CALL TO self.print_maze() AND DEF

        self.print_maze()

    def print_maze(self) -> None:
        for line in self.maze.values:
            for char in line:
                print(f"{char:x}" if char != 0xF else "_", end="")
            print()
        print("\n\n")
