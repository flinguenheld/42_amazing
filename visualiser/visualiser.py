from maze import Maze
from textual.widgets import Footer, Header, Digits
from textual.app import App, ComposeResult

from visualiser.tcell import TCell
from visualiser.tmaze import TMaze


class Visualiser(App):
    # CSS_PATH = "style_tuto.tcss"
    CSS_PATH = "style/cell.tcss"

    BINDINGS = [("t", "next_theme", "Next theme")]

    def __init__(self, maze: Maze) -> None:
        super().__init__()
        self.maze = TMaze(maze)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield self.maze

    def to_test(self):
        self.maze.update_cells()

    # def on_click(self) -> None:
    #     self.maze.update_cells()

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
