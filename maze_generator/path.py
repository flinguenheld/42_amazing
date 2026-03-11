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


class FullPath:
    """
    - Class that stores both a list of Paths
                And a flattened set of said list
    """

    def __init__(self) -> None:
        self.full_path: List[Path] = list()
        self.full_path_flat: Set[Tuple[int, int]] = set()

    def __getitem__(self, index) -> Path:
        return self.full_path[index]

    def __len__(self) -> int:
        return len(self.full_path)

    def append(self, path: Path) -> List[Tuple[int, int]]:
        self.full_path.append(path)
        for coor in path:
            self.full_path_flat.add(coor)
        return path

    def get_list(self) -> List[Path]:
        return self.full_path

    def get_set(self) -> Set[Tuple[int, int]]:
        return self.full_path_flat
