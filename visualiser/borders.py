from itertools import pairwise
from ast import Dict
from typing import List


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀█░█▀▄░█▀▄░█▀▀░█▀▄░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█░█░█▀▄░█░█░█▀▀░█▀▄░▀▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░▀▀▀
class Borders:
    def __init__(self):
        self.__current = "simple"
        self.__borders: Dict[str, List[str]] = {}
        self.__init_borders()

    def get_current(self) -> str:
        return self.__current

    def next(self) -> None:
        for a, b in pairwise(self.__borders.keys()):
            if a == self.__current:
                self.__current = b
                return
        self.__current = next(iter(self.__borders))

    def get_char(self, index: int) -> str:
        return self.__borders[self.__current][index]

    # #################################################### INITIALISATION ####
    def __init_borders(self) -> None:
        self.__borders["simple"] = [
            "━",  # 0
            "┃",  # 1
            "┣",  # 2
            "┫",  # 3
            "╋",  # 4
            "┳",  # 5
            "┻",  # 6
            "┏",  # 7
            "┓",  # 8
            "┗",  # 9
            "┛",  # 10
            " ",  # 11
            "━",  # 12
            "━",  # 13
            "┃",  # 14
            "┃",  # 15
        ]
        self.__borders["double"] = [
            "═",  # 0
            "║",  # 1
            "╠",  # 2
            "╣",  # 3
            "╬",  # 4
            "╦",  # 5
            "╩",  # 6
            "╔",  # 7
            "╗",  # 8
            "╚",  # 9
            "╝",  # 10
            " ",  # 11
            "═",  # 12
            "═",  # 13
            "║",  # 14
            "║",  # 15
        ]
        self.__borders["block"] = [
            "▀",  # 0
            "█",  # 1
            "█",  # 2
            "█",  # 3
            "█",  # 4
            "█",  # 5
            "▀",  # 6
            "█",  # 7
            "█",  # 8
            "▀",  # 9
            "▀",  # 10
            " ",  # 11
            "▀",  # 12
            "▀",  # 13
            "█",  # 14
            "█",  # 15
        ]
