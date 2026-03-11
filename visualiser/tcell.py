from textual.reactive import reactive
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
    _to_print = reactive("")

    def __init__(self, borders: Borders) -> None:
        super().__init__()
        self._borders = borders

    @abstractmethod
    def refresh_cell(self) -> None:
        pass

    @abstractmethod
    def up_state(self, **values: bool) -> None:
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
        return self._to_print

    # ###################################################### REFRESH CELL ####
    def refresh_cell(self) -> None:
        match (self.top, self.right, self.bottom, self.left):
            case (False, True, False, True):
                self._to_print = self._borders.get_char(0)
            case (True, False, True, False):
                self._to_print = self._borders.get_char(1)
            case (True, True, True, False):
                self._to_print = self._borders.get_char(2)
            case (True, False, True, True):
                self._to_print = self._borders.get_char(3)
            case (True, True, True, True):
                self._to_print = self._borders.get_char(4)
            case (False, True, True, True):
                self._to_print = self._borders.get_char(5)
            case (True, True, False, True):
                self._to_print = self._borders.get_char(6)
            case (False, True, True, False):
                self._to_print = self._borders.get_char(7)
            case (False, False, True, True):
                self._to_print = self._borders.get_char(8)
            case (True, True, False, False):
                self._to_print = self._borders.get_char(9)
            case (True, False, False, True):
                self._to_print = self._borders.get_char(10)

            # Extend horizontal walls in the angle
            # TODO: Keep the 12 / 13 / 14 / 15 ???
            case (False, True, False, False):
                self._to_print = self._borders.get_char(12)
            case (False, False, False, True):
                self._to_print = self._borders.get_char(13)

            # Extend vertical walls in the angle
            case (True, False, False, False):
                self._to_print = self._borders.get_char(14)
            case (False, False, True, False):
                self._to_print = self._borders.get_char(15)

            case _:
                self._to_print = self._borders.get_char(11)

    # ########################################################## UP STATE ####
    def up_state(self, **values: bool) -> None:
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

    # ###################################################### REFRESH CELL ####
    def refresh_cell(self) -> None:
        if self.active:
            self._to_print = self._borders.get_char(0) * 3
        else:
            self._to_print = self._borders.get_char(11) * 3

    # ########################################################## UP STATE ####
    def up_state(self, **values: bool) -> None:
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
        return self._to_print

    # ###################################################### REFRESH CELL ####
    def refresh_cell(self) -> None:
        if self.active:
            self._to_print = self._borders.get_char(1)
        else:
            self._to_print = self._borders.get_char(11)

    # ########################################################## UP STATE ####
    def up_state(self, **values: bool) -> None:
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
        return self._to_print

    # ###################################################### REFRESH CELL ####
    def refresh_cell(self) -> None:
        if self.value == 0:
            self._to_print = "   "
        else:
            self._to_print = "   "
