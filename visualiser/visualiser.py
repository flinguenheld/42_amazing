from typing import ClassVar, Dict, Any
from textual.binding import Binding, BindingType

from mazegen.config import Config

from visualiser.tmaze import TMaze
from visualiser.ttitle import TTitle
from visualiser.tconfig import TConfig

from textual import events
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
        ("n", "next_step", "Next step"),
        ("a", "animate", "Animate"),
        ("r", "restart", "Restart player"),
        ("t", "next_theme", "Next theme"),
        ("c", "config", "Config"),
        ("f", "forty_two", "42"),
        ("up", "ignore", ""),
        ("down", "ignore", ""),
        ("left", "ignore", ""),
        ("right", "ignore", ""),
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
            with ScrollableNoArrow(id="scroll_layout"):
                yield self.__tmaze

    # ########################################################################
    # ############################################################ MOUNT #####
    async def on_mount(self, blah: ScreenResultType) -> None:
        self.title = "a_maze_ing"
        self.action_next_theme()
        self.action_generate_new_maze()
        self.set_interval(10, self.action_forty_two)

    # ########################################################################
    # ######################################################## MOVEMENTS #####
    def on_key(self, event: events.Key) -> None:
        self.__tmaze.move_player(event.key)

    # ########################################################################
    # ################################################# ACTION - OPTIONS #####
    def action_restart(self) -> None:
        self.__tmaze.player_clean()
        self.__tmaze.player_reset()

    # ########################################################################
    # ###################################################### ACTION - 42 #####
    async def action_forty_two(self) -> None:
        await self.__tmaze.run_forty_two()

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
    def action_generate_new_maze(self) -> None:
        self.__tmaze.generate_new_maze()

    # ########################################################################
    # ############################################### ACTION - ANIMATION #####
    def action_start_new_maze(self) -> None:
        self.__tmaze.start_new_maze()

    async def action_animate(self) -> None:
        await self.__tmaze.animate_all_steps()

    def action_next_step(self) -> None:
        self.__tmaze.next_step_animation()

    # ########################################################################
    # ########################################################### THEMES #####
    def __get_colours(self) -> Dict[Any, Any]:
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


# ############################################################################
# ############################################################################
# ######################################## PREVENT SCROLLING WITH ARROWS #####
class ScrollableNoArrow(ScrollableContainer):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("up", "ignore", "Scroll Up", show=False),
        Binding("down", "ignore", "Scroll Down", show=False),
        Binding("left", "ignore", "Scroll Left", show=False),
        Binding("right", "ignore", "Scroll Right", show=False),
        Binding("home", "scroll_home", "Scroll Home", show=False),
        Binding("end", "scroll_end", "Scroll End", show=False),
        Binding("pageup", "page_up", "Page Up", show=False),
        Binding("pagedown", "page_down", "Page Down", show=False),
        Binding("ctrl+pageup", "page_left", "Page Left", show=False),
        Binding("ctrl+pagedown", "page_right", "Page Right", show=False),
    ]
