from textual.containers import (
    VerticalGroup,
)
from textual.widgets import Footer, Header
from textual.app import App, ComposeResult

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
        ("m", "new_maze", "New maze"),
    ]

    def __init__(self, config) -> None:
        super().__init__()
        self.__borders = Borders()
        self.__tmaze = TMaze(config, self.__borders)
        self.__title = TTitle()
        self.__config_TO_REMOVE = config
        self.action_new_maze()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalGroup(id="main_layout"):
            yield self.__title
            yield self.__tmaze
        yield Footer()

    # ########################################################################
    # ########################################################### THEMES #####
    def action_new_maze(self):
        self.__tmaze.new_maze(self.__config_TO_REMOVE)

    # ########################################################################
    # ########################################################## BORDERS #####
    def action_border(self) -> None:
        self.__borders.next()
        self.__tmaze.refresh_maze()

    # ########################################################################
    # ########################################################### THEMES #####
    def on_mount(self) -> None:
        self.action_next_theme()

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
