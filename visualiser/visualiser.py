from textual.containers import (
    VerticalGroup,
    Center,
    Right,
    Horizontal,
    CenterMiddle,
)
from maze import Maze
from textual.widgets import Footer, Header, Digits, Label
from textual.app import App, ComposeResult

from visualiser.tcell import TCell
from visualiser.tmaze import TMaze
from visualiser.ttitle import TTitle
from visualiser.borders import Borders


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░▀█▀░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░█░░▀▀█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀
class Visualiser(App):
    CSS_PATH = ["style/main.tcss"]
    BINDINGS = [
        ("t", "next_theme", "Next theme"),
        ("b", "border", "Next border"),
    ]

    def __init__(self, maze: Maze) -> None:
        super().__init__()
        self.__borders = Borders()
        self.__maze = TMaze(maze, self.__borders)
        self.__title = TTitle()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalGroup(id="main_layout"):
            yield self.__title
            yield self.__maze
        yield Footer()

    def refresh_maze(self) -> None:
        self.__maze.update_cells_state()
        self.__maze.refresh_cells()

    # ########################################################################
    # ########################################################## BORDERS #####
    def action_border(self) -> None:
        self.__borders.next()
        self.refresh_maze()

    # ########################################################################
    # ########################################################### THEMES #####
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
