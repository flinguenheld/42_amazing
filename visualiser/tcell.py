from typing import List
from abc import abstractmethod
from textual.widgets import Static
from textual.app import RenderResult

from visualiser.borders import Borders


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class TCell(Static):
    def __init__(self, borders: Borders) -> None:
        super().__init__()
        self._borders = borders

    @abstractmethod
    def up_value(self, **values: bool) -> None:
        pass


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░░░░█▀█░█▀█░█▀▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░░░░█▀█░█░█░█░█░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀▀▀
class TCellAngle(TCell):
    def __init__(self, borders: Borders) -> None:
        super().__init__(borders)
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False

    def render(self) -> RenderResult:
        match (self.top, self.right, self.bottom, self.left):
            case (False, True, False, True):
                return self._borders.get_char(0)
            case (True, False, True, False):
                return self._borders.get_char(1)
            case (True, True, True, False):
                return self._borders.get_char(2)
            case (True, False, True, True):
                return self._borders.get_char(3)
            case (True, True, True, True):
                return self._borders.get_char(4)
            case (False, True, True, True):
                return self._borders.get_char(5)
            case (True, True, False, True):
                return self._borders.get_char(6)
            case (False, True, True, False):
                return self._borders.get_char(7)
            case (False, False, True, True):
                return self._borders.get_char(8)
            case (True, True, False, False):
                return self._borders.get_char(9)
            case (True, False, False, True):
                return self._borders.get_char(10)

            # Extend horizontal walls in the angle
            case (False, True, False, False):
                return self._borders.get_char(0)
            case (False, False, False, True):
                return self._borders.get_char(0)

            # Extend vertical walls in the angle
            case (True, False, False, False):
                return self._borders.get_char(1)
            case (False, False, True, False):
                return self._borders.get_char(1)

            case _:
                return self._borders.get_char(11)

    def up_value(self, **values: bool) -> None:
        print(f"up values: {values}")
        if "top" in values.keys() and values["top"]:
            self.top = True
        if "bottom" in values.keys() and values["bottom"]:
            self.bottom = True
        if "right" in values.keys() and values["right"]:
            self.right = True
        if "left" in values.keys() and values["left"]:
            self.left = True


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░░░░█░█░█▀█░█▀▄░▀█▀░▀▀█░█▀█░█▀█░▀█▀░█▀█░█░░
# ░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░░░░█▀█░█░█░█▀▄░░█░░▄▀░░█░█░█░█░░█░░█▀█░█░░
# ░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀░▀░▀▀▀
class TCellHorizontal(TCell):
    def __init__(self, borders: Borders) -> None:
        super().__init__(borders)
        self.active = False

    def render(self) -> RenderResult:
        if self.active:
            return self._borders.get_char(0) * 3
        return self._borders.get_char(11) * 3

    def up_value(self, **values: bool) -> None:
        if "active" in values.keys() and values["active"]:
            self.active = True


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░░░░█░█░█▀▀░█▀▄░▀█▀░▀█▀░█▀▀░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░░░░▀▄▀░█▀▀░█▀▄░░█░░░█░░█░░░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀
class TCellVertical(TCell):
    def __init__(self, borders: Borders) -> None:
        super().__init__(borders)
        self.active = False

    def render(self) -> RenderResult:
        if self.active:
            return self._borders.get_char(1)
        return self._borders.get_char(11)

    def up_value(self, **values: bool) -> None:
        if "active" in values.keys() and values["active"]:
            self.active = True


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░░░░█▄█░▀█▀░█▀▄░█▀▄░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░░░░█░█░░█░░█░█░█░█░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀▀░░▀▀░░▀▀▀░▀▀▀
class TCellMiddle(TCell):
    def __init__(self, borders: Borders) -> None:
        super().__init__(borders)
        self.value = 0

    def render(self) -> RenderResult:
        if self.value == 0:
            return "   "
        return " o "
