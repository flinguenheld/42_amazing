from maze import Maze
from typing import List, Tuple, Set, Dict


class Path:
    """
    - Simple class that stores path related info
    - Allows to access actual path (list of coordinates) via index
    """

    WALL_MAP: Dict[Tuple[int, int], int] = {
        (-1, 0): 0b0001,
        (0, 1): 0b0010,
        (1, 0): 0b0100,
        (0, -1): 0b1000,
    }

    def __init__(
        self,
        path_start: List[Tuple[int, int]],
    ) -> None:
        self.values: Dict[Tuple[int, int], int] = dict()
        self.path: List[Tuple[int, int]] = path_start

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
            value = value & ~(self.WALL_MAP.get(offset, 0))
        return value

    def __get_last_value(self, maze: Maze) -> None:
        r, c = self.path[-1]
        prev_r, prev_c = self.path[-2]
        offset = (r - prev_r, c - prev_c)
        maze.values[prev_r][prev_c] = maze.values[prev_r][prev_c] & ~(
            self.WALL_MAP.get(offset, 0)
        )
        offset = (prev_r - r, prev_c - c)
        maze.values[r][c] = maze.values[r][c] & ~(self.WALL_MAP.get(offset, 0))

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
        self.full_path: List[Path] = list()
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
