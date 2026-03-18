from typing import Any, List
from mazegen.path import Path

from datetime import datetime
import time


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░
class Maze:
    """Class that stores maze related parameters and states

    - Public attributes:
        WALL_MAP: Correspondance from moves to binary
        LETTER_MAP: Correspondance from moves to letters
        nb_row: int, number of rows
        nb_col: int, number of cols
        entry: tuple[int, int], entry coordinates
        exit: tuple[int, int], exit coordinates
        perfect: bool, perfect character (unique path from any (Ax, Ay)
                                                            to any (Bx, By))
        seed: any, data for reproductability
        loop_ratio: int, from 0 to 100, amount of broken
                                                walls if perfect = False
        values: List[List[int]], two-dimensional array of hexadecimal values,
                                  each cell representing 4 of the maze's walls
        cells_42: List[tuple[int, int]], list of coordinates belonging
                                                                to the 42 logo
    """

    WALL_MAP = {
        (-1, 0): 0b0001,
        (0, 1): 0b0010,
        (1, 0): 0b0100,
        (0, -1): 0b1000,
    }

    LETTER_MAP = {
        (-1, 0): "N",
        (0, 1): "E",
        (1, 0): "S",
        (0, -1): "W",
    }

    def __init__(
        self,
        nb_row: int,
        nb_col: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
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
            self.seed: Any = (
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}AUTO{time.time()}"
            )
        else:
            self.seed = seed
        self.solution: List[tuple[int, int]] = []
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
        else:
            self.cells_42 = set()

    def break_wall(
        self, cell1: tuple[int, int], cell2: tuple[int, int], safe: bool
    ) -> None:
        """Breaks wall between passed coordinates wall in self.values,
        possibly safely"""
        if cell1 == cell2:
            return
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
        """Setter for self.solution"""
        self.solution = path.get_list()

    def __str__(self) -> str:
        """Representation of values, entry/exit and solution
        as a single string"""
        res = ""
        for line in self.values:
            for char in line:
                res = f"{res}{char:X}"
            res = f"{res}\n"
        res = f"{res}\n\n{self.start}\n{self.end}\n"
        if getattr(self, "solution") is not None:
            for i in range(len(self.solution) - 2):
                cur = self.solution[i]
                nxt = self.solution[i + 1]
                to_print: str = self.LETTER_MAP[
                    (nxt[0] - cur[0], cur[1] - nxt[1])
                ]
                res = f"{res}{to_print}"
        res = f"{res}\n"

        return res
