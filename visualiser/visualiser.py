from textual.color import Color
from visualiser.tmaze import TMaze
from visualiser.ttitle import TTitle
from visualiser.toptions import TOptions
from textual.widgets import Footer, Header
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Vertical


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░▀█▀░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░█░░▀▀█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀
class Visualiser(App[None]):
    CSS_PATH = ["style/main.tcss", "style/options.tcss"]
    BINDINGS = [
        ("t", "next_theme", "Next theme"),
        ("g", "generate_new_maze", "Generate a new maze"),
        ("s", "start_new_maze", "Start a new maze"),
        ("a", "animate", "Animate"),
        ("n", "next_step", "Next step"),
        ("o", "options", "Options"),
    ]

    def __init__(self, config) -> None:
        super().__init__()
        self.theme = "gruvbox"
        self.__ttitle = TTitle()
        self.__config_TO_REMOVE = config
        self.__tmaze = TMaze(config, self.__get_colours())

    # ########################################################################
    # ########################################################## COMPOSE #####
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Vertical(id="main_layout"):
            yield self.__ttitle
            with ScrollableContainer(id="scroll_layout"):
                yield self.__tmaze

    # ########################################################################
    # ############################################################ MOUNT #####
    async def on_mount(self) -> None:
        self.title = "a_maze_ing"
        self.action_next_theme()
        self.action_generate_new_maze()

    # ########################################################################
    # ################################################# ACTION - OPTIONS #####
    def action_options(self):
        self.push_screen(TOptions())

    # ########################################################################
    # ################################################ ACTION - NEW MAZE #####
    def action_generate_new_maze(self):
        self.__tmaze.generate_new_maze()

    # ########################################################################
    # ############################################### ACTION - ANIMATION #####
    def action_start_new_maze(self):
        self.__tmaze.start_new_maze()

    async def action_animate(self):
        await self.__tmaze.animate_all_steps()

    def action_next_step(self):
        self.__tmaze.next_step_animation()

    # ########################################################################
    # ########################################################### THEMES #####
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

        self.__tmaze.up_colours(self.__get_colours())
