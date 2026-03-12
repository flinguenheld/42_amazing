from abc import abstractmethod, ABC
from typing import Set, Tuple, Dict
from visualiser.borders import Borders


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀▀░█▀▀░█░░░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█▀▀░█░░░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class MCell(ABC):
    def __init__(self, borders: Borders) -> None:
        self._borders = borders

    @abstractmethod
    def to_str(self, row: int, col: int) -> str:
        pass


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀▀░█▀▀░█░░░█░░░░░█░█░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█▀▀░█░░░█░░░░░█▀█░▀▄▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░░▀░
class MCellHV(MCell):
    def __init__(self, borders: Borders) -> None:
        super().__init__(borders)
        self._list: Set[Tuple[int, int]] = set()

    def add(self, row: int, col: int, is_active: bool) -> None:
        if is_active:
            self._list.add((row, col))


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░█▄█░█▀▀░█▀▀░█░░░█░░░░░█░█░█▀█░█▀▄░▀█▀░▀▀█░█▀█░█▀█░▀█▀░█▀█░█░░
# ░░░░░░░░░░░░░░░█░█░█░░░█▀▀░█░░░█░░░░░█▀█░█░█░█▀▄░░█░░▄▀░░█░█░█░█░░█░░█▀█░█░░
# ░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀░▀░▀▀▀
class MCellHorizontal(MCellHV):
    def __init__(self, borders: Borders) -> None:
        super().__init__(borders)

    def to_str(self, row: int, col: int) -> str:
        if (row, col) in self._list:
            return self._borders.get_char(0) * 3
        else:
            return self._borders.get_char(11) * 3


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀▀░█▀▀░█░░░█░░░░░█░█░█▀▀░█▀▄░▀█▀░▀█▀░█▀▀░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█▀▀░█░░░█░░░░░▀▄▀░█▀▀░█▀▄░░█░░░█░░█░░░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀
class MCellVertical(MCellHV):
    def __init__(self, borders: Borders) -> None:
        super().__init__(borders)

    def to_str(self, row: int, col: int) -> str:
        if (row, col) in self._list:
            return self._borders.get_char(1)
        else:
            return self._borders.get_char(11)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀█░█▀▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░█░█░█░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀▀▀
class Angle:
    """
    Allow you to deal with all angle representations such as:
            ┣ ┫ ╋ ┳ ┻ ┏ ┓ ┗ ┛
    """

    def __init__(self, borders: Borders):
        self.__top = False
        self.__left = False
        self.__right = False
        self.__bottom = False
        self.__borders = borders

    def up(self, **who: bool):
        if "top" in who.keys() and who["top"]:
            self.__top = True
        if "left" in who.keys() and who["left"]:
            self.__left = True
        if "right" in who.keys() and who["right"]:
            self.__right = True
        if "bottom" in who.keys() and who["bottom"]:
            self.__bottom = True

    def __str__(self) -> str:
        match (self.__top, self.__right, self.__bottom, self.__left):
            case (False, True, False, True):
                return self.__borders.get_char(0)
            case (True, False, True, False):
                return self.__borders.get_char(1)
            case (True, True, True, False):
                return self.__borders.get_char(2)
            case (True, False, True, True):
                return self.__borders.get_char(3)
            case (True, True, True, True):
                return self.__borders.get_char(4)
            case (False, True, True, True):
                return self.__borders.get_char(5)
            case (True, True, False, True):
                return self.__borders.get_char(6)
            case (False, True, True, False):
                return self.__borders.get_char(7)
            case (False, False, True, True):
                return self.__borders.get_char(8)
            case (True, True, False, False):
                return self.__borders.get_char(9)
            case (True, False, False, True):
                return self.__borders.get_char(10)

            # Extend horizontal walls in the angle
            # TODO: Keep the 12 / 13 / 14 / 15 ???
            case (False, True, False, False):
                return self.__borders.get_char(12)
            case (False, False, False, True):
                return self.__borders.get_char(13)

            # Extend vertical walls in the angle
            case (True, False, False, False):
                return self.__borders.get_char(14)
            case (False, False, True, False):
                return self.__borders.get_char(15)

            case _:
                return self.__borders.get_char(11)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀▀░█▀▀░█░░░█░░░░░█▀█░█▀█░█▀▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█▀▀░█░░░█░░░░░█▀█░█░█░█░█░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀▀▀
class MCellAngle(MCell):
    def __init__(self, borders: Borders) -> None:
        super().__init__(borders)
        self.__angles: Dict[Tuple[int, int], Angle] = dict()

    def up(self, row: int, col: int, **who: bool):
        if (row, col) not in self.__angles:
            self.__angles.update({(row, col): Angle(self._borders)})

        self.__angles[(row, col)].up(**who)

    def to_str(self, row: int, col: int) -> str:
        if (row, col) in self.__angles:
            return str(self.__angles[(row, col)])
        else:
            return "X"
