from typing import Tuple
from mazegen.path import Path

from datetime import datetime
import time


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░
class Maze:
    """
    - Maze class that stores all maze related info:
        - Size
        - Start/End
        - List[List[]] of cell's values
        - List[] of coordinates of cells needed for logo
    - Has a break_wall method that clears path between cell1 and cell2
    """

    WALL_MAP = {
        (-1, 0): 0b0001,
        (0, 1): 0b0010,
        (1, 0): 0b0100,
        (0, -1): 0b1000,
    }

    def __init__(
        self,
        nb_row: int,
        nb_col: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool,
        seed: str,
        loop_ratio: int,
    ) -> None:
        """
        - Initializes with all needed values
        - If config gave no seed, define it with
                             mix of datetime.now() and time.time()
        - If size allows it, define in-logo cells
                and adjust start/end to prevent disconnected cells
        """
        self.nb_col = nb_col
        self.nb_row = nb_row
        self.start = entry
        self.end = exit
        self.perfect = perfect
        if seed is None:
            self.seed = (
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}AUTO{time.time()}"
            )
        else:
            self.seed = seed
        self.solution = None
        self.loop_ratio = loop_ratio
        self.values = [
            [0xF for _ in range(0, self.nb_col)] for _ in range(0, self.nb_row)
        ]
        mid_r, mid_c = (int((self.nb_row - 1) / 2), int((self.nb_col - 1) / 2))
        if nb_col >= 10 and nb_row >= 10:
            self.cells_42 = {
                # 4
                (mid_r - 2, mid_c - 3),
                (mid_r - 1, mid_c - 3),
                (mid_r, mid_c - 3),
                (mid_r, mid_c - 2),
                (mid_r, mid_c - 1),
                (mid_r + 1, mid_c - 1),
                (mid_r + 2, mid_c - 1),
                # 2
                (mid_r - 2, mid_c + 1),
                (mid_r - 2, mid_c + 2),
                (mid_r - 2, mid_c + 3),
                (mid_r - 1, mid_c + 3),
                (mid_r, mid_c + 3),
                (mid_r, mid_c + 2),
                (mid_r, mid_c + 1),
                (mid_r + 1, mid_c + 1),
                (mid_r + 2, mid_c + 1),
                (mid_r + 2, mid_c + 2),
                (mid_r + 2, mid_c + 3),
            }
            self.start = (mid_r - 1, mid_c + 2)
            self.end = (mid_r + 1, mid_c + 2)
        else:
            self.cells_42 = set()

    def break_wall(
        self, cell1: Tuple[int, int], cell2: Tuple[int, int], safe: bool
    ) -> None:
        """
        - Receives two Tuples of coordinates mapping to cells in maze.values
        - In safe mode: Clears path if doing so doesnt imply creating a 0 cell
        - Else: Just clears path
        """
        cells = [cell1, cell2]
        for cell in cells:
            ocell = [ocell for ocell in cells if ocell != cell][0]
            offset = (ocell[0] - cell[0], ocell[1] - cell[1])
            value = self.values[cell[0]][cell[1]]
            match safe:
                case True:
                    if value & ~(self.WALL_MAP.get(offset, 0)) > 0:
                        self.values[cell[0]][cell[1]] = value & ~(
                            self.WALL_MAP.get(offset, 0)
                        )
                case False:
                    self.values[cell[0]][cell[1]] = value & ~(
                        self.WALL_MAP.get(offset, 0)
                    )

    def set_solution(self, path: Path) -> None:
        """ Setter for self.solution """
        self.solution = path

    def __str__(self) -> str:
        """
        - Representation of self.values as a single string
        """
        res = ""
        for line in self.values:
            for char in line:
                res = f"{res}{char:X}"
            res = f"{res}\n"
        return res
