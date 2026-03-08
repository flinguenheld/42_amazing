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

    # TODO: ADD COLOR LOGIC ##################################################

    # TODO: REMOVE THAT ######################################################
    def set_wall(self, value: int) -> None:
        for css_class in self.classes:
            self.remove_class(css_class)

        self.add_class("wall")

        match value:
            case 0:
                self.add_class("wall_top")
            case 1:
                self.add_class("wall_bottom")
