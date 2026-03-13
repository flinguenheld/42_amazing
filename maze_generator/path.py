from typing import List, Tuple, Dict


class Path:
    """
    - Simple class that stores path related info
    - Allows to access actual path (list of coordinates) via index
    - Has a go_back method to revert path list to given coordinates
    """

    def __init__(
        self,
        path_start: List[Tuple[int, int]],
    ) -> None:
        self.path: List[Tuple[int, int]] = path_start

    def __getitem__(self, index: int) -> Tuple[int, int]:
        return self.path[index]

    def __len__(self) -> int:
        return len(self.path)

    def append(self, coor: Tuple[int, int]) -> None:
        self.path.append(coor)

    def go_back(self, target: Tuple[int, int]) -> None:
        index = [k for k, v in enumerate(self.path) if v == target][0]
        self.path = self.path[: index + 1]
