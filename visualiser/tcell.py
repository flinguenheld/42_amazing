from abc import abstractmethod
from textual.widgets import Static
from textual.app import RenderResult
from textual import log


class TCell(Static):
    # CSS_PATH = "style/cell.tcss"
    def __init__(self) -> None:
        super().__init__()

    # @abstractmethod
    def up_value(self, value: int | bool):
        self.__value = value


class TCellAngle(TCell):
    def __init__(self) -> None:
        super().__init__()
        self.value = 0

    def render(self) -> RenderResult:

        blah = [
            " ",
            " ",
            " ",
            "┓",
            " ",
            "┃",
            "┛",
            "┫",
            " ",
            "┏",
            "━",
            "┳",
            "┗",
            "┣",
            "┻",
            "╋",
        ]
        return blah[self.value]

        # #                  wsen
        # if self.value == 0b0110:
        #     return "┏"
        # if self.value == 0b1100:
        #     return "┓"
        # if self.value == 0b1010:
        #     return "┛"
        # if self.value == 0b0001:
        #     return "┗"
        # if self.value == 0b1011:
        #     return "┻"
        # if self.value == 0b1101:
        #     return "┳"

        # if self.value == 0b0111:
        #     return "┣"
        # if self.value == 0b1110:
        #     return "┫"

        # if self.value == 0b1111:
        #     return "╋"
        # if self.value == 0b0101:
        #     return "┃"
        # if self.value == 0b1010:
        #     return "━"

        # return " "

    def up_value(self, value: int):
        # log(f"value: {value} -> {self.value}")
        self.value |= value
        print(f"value: {value:04b} -> {self.value:04b}")


class TCellHorizontal(TCell):
    def __init__(self) -> None:
        super().__init__()
        self.value = False

    def render(self) -> RenderResult:
        if self.value:
            return "   "
        return "━━━"

    # def up_value(self, value: int | bool):
    #     self.value = value


class TCellVertical(TCell):
    def __init__(self) -> None:
        super().__init__()
        self.value = False

    def render(self) -> RenderResult:
        if self.value:
            return " "
        return "┃"

    # def up_value(self, value: int | bool):
    #     self.value = value


class TCellMiddle(TCell):
    def __init__(self) -> None:
        super().__init__()
        self.value = 0

    def render(self) -> RenderResult:
        if self.value == 0:
            return "   "
        return " o "

    # def up_value(self, value: int | bool):
    #     self.value = value
