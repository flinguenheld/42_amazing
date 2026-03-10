from textual.containers import VerticalGroup, Center, Right
from maze import Maze
from textual.widgets import Footer, Header, Digits, Label
from textual.app import App, ComposeResult

from visualiser.tcell import TCell
from visualiser.tmaze import TMaze
from visualiser.ttitle import TTitle


class Visualiser(App):
    CSS_PATH = ["style/main.tcss", "style/cell.tcss"]
    BINDINGS = [("t", "next_theme", "Next theme")]

    def __init__(self, maze: Maze) -> None:
        super().__init__()
        self.maze = TMaze(maze)
        self.__title = TTitle()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalGroup(id="main_layout"):
            yield self.__title
            yield self.maze
        yield Footer()

    def to_test(self):
        self.maze.update_cells()

    # #########################################################################
    # ############################################################ THEMES #####
    def on_mount(self) -> None:
        self.action_next_theme()

    # def on_key(self, event: events.Key) -> None:
    #     if event.key.isdecimal():
    #         self.action_next_theme()

    def action_next_theme(self) -> None:
        """Change theme"""

        match self.theme[-5:]:
            case "uvbox":
                self.theme = "catppuccin-latte"
            case "latte":
                self.theme = "catppuccin-macchiato"
            case "hiato":
                self.theme = "catppuccin-mocha"
            case "mocha":
                self.theme = "catppuccin-frappe"
            case _:
                self.theme = "gruvbox"
