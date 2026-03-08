from textual.widgets import Static
from textual.app import RenderResult


class TCell(Static):
    # CSS_PATH = "style/cell.tcss"
    def __init__(self) -> None:
        super().__init__()
        self.value = 0

    def render(self) -> RenderResult:
        # TODO: Add here all options according to the cell value
        if self.value == 5:
            return "a"
        else:
            return "-"


class TCellAngle(TCell):
    def render(self) -> RenderResult:
        if self.value == 0:
            return " "
        return "+"


class TCellHorizontal(TCell):
    def render(self) -> RenderResult:
        if self.value == 0:
            return " "
        return "-"


class TCellVertical(TCell):
    def render(self) -> RenderResult:
        if self.value == 0:
            return " "
        return "|"


class TCellMiddle(TCell):
    def render(self) -> RenderResult:
        if self.value == 0:
            return " "
        return "o"
