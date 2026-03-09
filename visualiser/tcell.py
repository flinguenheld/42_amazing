from typing import List
from abc import abstractmethod
from textual.widgets import Static
from textual.app import RenderResult


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class TCell(Static):
    def __init__(self) -> None:
        super().__init__()
        self._borders: List[str] = [
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
        ]

    @abstractmethod
    def up_value(self, **values: bool) -> None:
        pass


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░░░░█▀█░█▀█░█▀▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░░░░█▀█░█░█░█░█░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀▀▀
class TCellAngle(TCell):
    def __init__(self) -> None:
        super().__init__()
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False

    def render(self) -> RenderResult:
        match (self.top, self.right, self.bottom, self.left):
            case (False, True, False, True):
                return self._borders[0]
            case (True, False, True, False):
                return self._borders[1]
            case (True, True, True, False):
                return self._borders[2]
            case (True, False, True, True):
                return self._borders[3]
            case (True, True, True, True):
                return self._borders[4]
            case (False, True, True, True):
                return self._borders[5]
            case (True, True, False, True):
                return self._borders[6]
            case (False, True, True, False):
                return self._borders[7]
            case (False, False, True, True):
                return self._borders[8]
            case (True, True, False, False):
                return self._borders[9]
            case (True, False, False, True):
                return self._borders[10]
            case _:
                return self._borders[11]

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
    def __init__(self) -> None:
        super().__init__()
        self.active = False

    def render(self) -> RenderResult:
        if self.active:
            return self._borders[0] * 3
        return self._borders[11] * 3

    def up_value(self, **values: bool) -> None:
        if "active" in values.keys() and values["active"]:
            self.active = True


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░░░░█░█░█▀▀░█▀▄░▀█▀░▀█▀░█▀▀░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░░░░▀▄▀░█▀▀░█▀▄░░█░░░█░░█░░░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀
class TCellVertical(TCell):
    def __init__(self) -> None:
        super().__init__()
        self.active = False

    def render(self) -> RenderResult:
        if self.active:
            return self._borders[1]
        return self._borders[11]

    def up_value(self, **values: bool) -> None:
        if "active" in values.keys() and values["active"]:
            self.active = True


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█░░░█░░░░░█▄█░▀█▀░█▀▄░█▀▄░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀▀░█░░░█░░░░░█░█░░█░░█░█░█░█░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀▀░░▀▀░░▀▀▀░▀▀▀
class TCellMiddle(TCell):
    def __init__(self) -> None:
        super().__init__()
        self.value = 0

    def render(self) -> RenderResult:
        if self.value == 0:
            return "   "
        return " o "
