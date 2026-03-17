from mazegen.config import Config

from visualiser.tmaze import TMaze
from visualiser.ttitle import TTitle
from visualiser.tconfig import TConfig

from textual.color import Color
from textual.widgets import Footer, Header
from textual.app import App, ComposeResult
from textual.screen import ScreenResultType
from textual.containers import ScrollableContainer, Vertical


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░▀█▀░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░█░░▀▀█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀
class Visualiser(App[None]):
    CSS_PATH = ["style/main.tcss", "style/config.tcss", "style/message.tcss"]
    BINDINGS = [
        ("g", "generate_new_maze", "Generate a new maze"),
        ("s", "start_new_maze", "Start a new maze"),
        ("t", "next_theme", "Next theme"),
        ("n", "next_step", "Next step"),
        ("a", "animate", "Animate"),
        ("c", "config", "Config"),
    ]

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.theme = "catppuccin-latte"
        self.__ttitle = TTitle()
        self.__config = config
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
    async def on_mount(self, blah: ScreenResultType) -> None:
        self.title = "a_maze_ing"
        self.action_next_theme()
        self.action_generate_new_maze()

    # ########################################################################
    # ################################################# ACTION - OPTIONS #####
    # TODO: KEEP THAT ?????
    def on_after_config(self) -> None:
        pass

    async def action_config(self) -> None:
        self.push_screen(
            TConfig(self.__config), callback=self.on_after_config()
        )

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
                "primary": Color.parse(theme.primary),
                "secondary": Color.parse(theme.secondary),
                "accent": Color.parse(theme.accent),
                "foreground": Color.parse(theme.foreground),
                "background": Color.parse(theme.background),
                "success": Color.parse(theme.success),
                "warning": Color.parse(theme.warning),
                "error": Color.parse(theme.error),
                "surface": Color.parse(theme.surface),
                "panel": Color.parse(theme.panel),
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
