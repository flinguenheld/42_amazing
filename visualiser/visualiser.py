from textual.theme import Theme
from textual.app import App, ComposeResult
from textual.color import Color

from textual_canvas import Canvas
import asyncio
from textual.containers import (
    VerticalGroup,
)
from textual.widgets import Footer, Header
from textual.app import App, ComposeResult

from visualiser.tmaze import TMaze
from visualiser.ttitle import TTitle
from visualiser.borders import Borders
from visualiser.canvas_test import CMaze


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░▀█▀░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░█░░▀▀█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀
class Visualiser(App[None]):
    CSS_PATH = ["style/main.tcss"]
    BINDINGS = [
        ("t", "next_theme", "Next theme"),
        ("b", "border", "Next border"),
        ("m", "new_maze", "New maze"),
        ("n", "next_step", "Next step"),
        ("a", "animate", "Animate"),
    ]

    def __init__(self, config) -> None:
        super().__init__()
        self.__borders = Borders()
        self.__tmaze = TMaze(config, self.__borders)
        self.__title = TTitle()
        self.__config_TO_REMOVE = config
        self.theme = "gruvbox"
        self.__canvas_test = CMaze(config, self.__get_colours())
        # self.__canvas_test.init_canvas()
        # self.action_new_maze()

        self.__tmaze.new_animation()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalGroup(id="main_layout"):
            yield self.__title
            yield self.__tmaze

        # yield Canvas(30, 30)
        yield self.__canvas_test
        yield Footer()

    # ########################################################################
    # ######################################################### NEW MAZE #####
    def action_new_maze(self):
        self.__canvas_test.generate_new_maze()

    def action_next_step(self):
        # self.__tmaze.next_step_animation()
        # self.__canvas_test.up_size(20, 20)
        # self.__canvas_test.refresh()
        # self.__canvas_test.up_canvas()
        self.__canvas_test.next_step_animation()

    # ########################################################################
    # ########################################################## ANIMATE #####
    async def action_animate(self):
        while self.__tmaze.next_step_animation():
            self.__tmaze.refresh()
            await asyncio.sleep(0.0005)

    # ########################################################################
    # ########################################################## BORDERS #####
    def action_border(self) -> None:
        self.__borders.next()
        self.__tmaze.refresh_maze_representation()

    # ########################################################################
    # ########################################################### THEMES #####
    def on_mount(self) -> None:
        self.action_next_theme()

    def __get_colours(self):

        theme = self.get_theme(self.theme)
        if theme:
            return {
                "background": Color.parse(theme.background),
                "primary": Color.parse(theme.primary),
                "secondary": Color.parse(theme.secondary),
            }
        return {}

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

        self.__canvas_test.up_colours(self.__get_colours())
