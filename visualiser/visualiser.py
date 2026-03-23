import asyncio
from mazegen.config import Config
from typing import ClassVar, Dict, Any


from visualiser.tmaze import TMaze
from visualiser.ttitle import TTitle
from visualiser.tconfig import TConfig
from visualiser.tbar import TBar

from textual.color import Color
from textual import events, work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.binding import Binding, BindingType
from textual.containers import ScrollableContainer, Vertical


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░▀█▀░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░█░░▀▀█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀
class Visualiser(App[None]):
    CSS_PATH = [
        "style/main.tcss",
        "style/config.tcss",
        "style/message.tcss",
        "style/bar.tcss",
    ]
    BINDINGS = [
        ("g", "generate_new_maze", "Generate a new maze"),
        ("s", "start_new_maze", "Start a new maze"),
        ("n", "next_step", "Next step"),
        ("a", "animate", "Animate"),
        ("q", "stop_animations", "Stop animation"),
        ("r", "restart", "Restart player"),
        ("w", "solution", "Run solution"),
        ("u", "solution_deactivate", "Clean solution"),
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
        self._ttitle = TTitle()
        self._config = config
        self._tbar = TBar(config)
        self._tmaze = TMaze(config, self._get_colours())

    # ########################################################################
    # ########################################################## COMPOSE #####
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Vertical(id="main_layout"):
            yield self._ttitle
            yield self._tbar
            with ScrollableNoArrow(id="scroll_layout"):
                yield self._tmaze

    # ########################################################################
    # ############################################################ MOUNT #####
    async def on_mount(self) -> None:
        self.title = "a_maze_ing"
        self.action_next_theme()
        self.action_generate_new_maze()
        self.set_interval(10, self.action_forty_two)

    # ########################################################################
    # ######################################################## MOVEMENTS #####
    def on_key(self, event: events.Key) -> None:
        self._tmaze.move_player(event.key)

    # ########################################################################
    # ################################################# ACTION - OPTIONS #####
    def action_restart(self) -> None:
        self._tmaze.player_clean()
        self._tmaze.player_reset()

    # ########################################################################
    # ################################################ ACTION - SOLUTION #####
    async def action_solution(self) -> None:
        asyncio.create_task(self._tmaze.solution_run())

    def action_solution_deactivate(self) -> None:
        self._tmaze.solution_deactivate()

    # ########################################################################
    # ###################################################### ACTION - 42 #####
    async def action_forty_two(self) -> None:
        await self._tmaze.forty_two_run()

    # ########################################################################
    # ################################################# ACTION - OPTIONS #####
    @work
    async def action_config(self) -> None:
        await self.app.push_screen_wait(TConfig(self._config))
        self._tbar.refresh_values()

    # ########################################################################
    # ################################################ ACTION - NEW MAZE #####
    def action_generate_new_maze(self) -> None:
        self._tbar.refresh_values()
        self._tmaze.generate_new_maze()

    # ########################################################################
    # ############################################### ACTION - ANIMATION #####
    def action_start_new_maze(self) -> None:
        self._tbar.refresh_values()
        self._tmaze.start_new_maze()

    async def action_animate(self) -> None:
        asyncio.create_task(self._tmaze.animate_all_steps())

    def action_next_step(self) -> None:
        self._tmaze.next_step_animation()

    def action_stop_animations(self) -> None:
        self._tmaze.stop_animations()

    # ########################################################################
    # ########################################################### THEMES #####
    def _get_colours(self) -> Dict[Any, Any]:
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

        self._tmaze.up_colours(self._get_colours())


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
