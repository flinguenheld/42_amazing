from textual.color import Color
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.containers import VerticalGroup

from visualiser.tmaze import TMaze
from visualiser.ttitle import TTitle


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
        self.theme = "gruvbox"
        self.__title = TTitle()
        self.__config_TO_REMOVE = config
        self.__canvas_test = TMaze(config, self.__get_colours())
        self.action_new_maze()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalGroup(id="main_layout"):
            yield self.__title
            yield self.__canvas_test
        yield Footer()

    # ########################################################################
    # ################################################ ACTION - NEW MAZE #####
    def action_new_maze(self):
        self.__canvas_test.generate_new_maze()

    # ########################################################################
    # ############################################### ACTION - NEXT STEP #####
    def action_next_step(self):
        self.__canvas_test.next_step_animation()

    # ########################################################################
    # ################################################# ACTION - ANIMATE #####
    async def action_animate(self):
        await self.__canvas_test.animate_all_steps()

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
