from typing import Tuple


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░
class Maze:
    def __init__(
        self,
        nb_row: int,
        nb_col: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool,
    ) -> None:
        self.nb_col = nb_col
        self.nb_row = nb_row
        self.start = entry
        self.end = exit
        self.perfect = perfect
        self.values = [
            [0xF for _ in range(0, self.nb_col)] for _ in range(0, self.nb_row)
        ]
        # self.TEST_MAZE()

    def TEST_MAZE(self):
        #     # self.values[0][0] = 0x9
        #     # self.values[0][1] = 0x3

        # BB577
        # DE7F7
        # BAEE3
        # D756A
        # FDD56

        self.values[0][0] = 0xB
        self.values[0][1] = 0xB
        self.values[0][2] = 0x5
        self.values[0][3] = 0x7
        self.values[0][4] = 0x7

        self.values[1][0] = 0xD
        self.values[1][1] = 0xE
        self.values[1][2] = 0x7
        self.values[1][3] = 0xF
        self.values[1][4] = 0x7

        self.values[2][0] = 0xB
        self.values[2][1] = 0xA
        self.values[2][2] = 0xE
        self.values[2][3] = 0xE
        self.values[2][4] = 0x3

        self.values[3][0] = 0xD
        self.values[3][1] = 0x7
        self.values[3][2] = 0x5
        self.values[3][3] = 0x6
        self.values[3][4] = 0xA

        self.values[4][0] = 0xF
        self.values[4][1] = 0xD
        self.values[4][2] = 0xD
        self.values[4][3] = 0x5
        self.values[4][4] = 0x6

    def __str__(self) -> str:
        res = ""
        for line in self.values:
            for char in line:
                res = f"{res}{char:X}"
            res = f"{res}\n"
        return res
