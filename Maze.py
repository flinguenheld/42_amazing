from typing import Tuple


class Maze:
    def __init__(self, nb_row: int, nb_col: int, 
                 start: Tuple[int, int], end: Tuple[int, int],
                 perfect: bool) -> None:
        self.nb_col = nb_col
        self.nb_row = nb_row
        self.start = start
        self.end = end
        self.perfect = perfect
        self.values = [[0xF for _ in range (0, self.nb_col)]
                       for _ in range(0, self.nb_row)]
        
    def __str__(self) -> str:
        res = ""
        for line in self.values:
            for char in line:
                res = f"{res}{char:X}"
            res = f"{res}\n"
        return res
