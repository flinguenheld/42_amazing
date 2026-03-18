from typing import List


class Path:
    """Simple class that stores path related info

    - Allows to access actual path (list of coordinates) via index
    - Has a go_back method to revert path list to given coordinates
    """

    def __init__(
        self,
        path_start: List[tuple[int, int]],
    ) -> None:
        self.path: List[tuple[int, int]] = path_start

    def __getitem__(self, index: int) -> tuple[int, int]:
        """Allow for access like Path[x]"""
        return self.path[index]

    def __len__(self) -> int:
        """Allow for len(Path)"""
        return len(self.path)

    def append(self, coor: tuple[int, int]) -> None:
        """Allow for Path.append()"""
        self.path.append(coor)

    def go_back(self, target: tuple[int, int]) -> None:
        """Reverse list to given index"""
        index = [k for k, v in enumerate(self.path) if v == target][0]
        self.path = self.path[: index + 1]

    def get_list(self) -> List[tuple[int, int]]:
        """Returns list for mypy..."""
        return self.path
