import asyncio
from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import HorizontalGroup, Horizontal, HorizontalScroll


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░░█░░░█░░█░█░█░█░▀▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀
class TActions(Static):
    def __init__(self) -> None:

        super().__init__()
        self._generate = Button(
            "(G)enerate",
            flat=True,
            variant="success",
            classes="bt_actions",
        )
        self._start = Button(
            "(S)tart new maze",
            flat=True,
            variant="warning",
            classes="bt_actions",
        )
        self._next_step = Button(
            "(N)ext",
            flat=True,
            variant="default",
            classes="bt_actions",
        )
        self._build_maze = Button(
            "(B)uild",
            flat=True,
            variant="default",
            classes="bt_actions",
        )
        self._stop_animation = Button(
            "Stop animation (Q)",
            flat=True,
            variant="primary",
            classes="bt_actions",
        )

        self._restart_player = Button(
            "(R)estart player",
            flat=True,
            variant="primary",
            classes="bt_actions",
        )

        self._solution = Button(
            "Solution (W)",
            flat=True,
            variant="error",
            classes="bt_actions",
        )
        self._solution_deactivate = Button(
            "Clean (U)",
            flat=True,
            variant="primary",
            classes="bt_actions",
        )

        self._forty_two = Button(
            "(F)orty-two",
            flat=True,
            variant="primary",
            classes="bt_actions",
        )

    # ########################################################################
    # ########################################################## COMPOSE #####
    def compose(self) -> ComposeResult:
        with HorizontalScroll(id="action_main_layout"):
            with HorizontalGroup(
                classes="action_layout_group action_layout_success"
            ):
                yield self._generate
            with Horizontal(
                classes="action_layout_group action_layout_warning"
            ):
                yield self._start
                yield self._next_step
                yield self._build_maze
            with HorizontalGroup(
                classes="action_layout_group action_layout_primary"
            ):
                yield self._stop_animation
            with HorizontalGroup(
                classes="action_layout_group action_layout_primary"
            ):
                yield self._restart_player
            with HorizontalGroup(
                classes="action_layout_group action_layout_error"
            ):
                yield self._solution
                yield self._solution_deactivate
            with HorizontalGroup(
                classes="action_layout_group action_layout_primary"
            ):
                yield self._forty_two

    # ########################################################################
    # ########################################################## ACTIONS #####
    async def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button == self._generate:
            self.app.action_generate_new_maze()  # type: ignore

        if event.button == self._start:
            self.app.action_start_new_maze()  # type: ignore

        if event.button == self._next_step:
            self.app.action_next_step()  # type: ignore

        if event.button == self._build_maze:
            asyncio.create_task(self.app.action_animate())  # type: ignore

        if event.button == self._stop_animation:
            self.app.action_stop_animations()  # type: ignore

        if event.button == self._restart_player:
            self.app.action_restart_player()  # type: ignore

        if event.button == self._solution:
            asyncio.create_task(self.app.action_solution())  # type: ignore

        if event.button == self._solution_deactivate:
            self.app.action_solution_deactivate()  # type: ignore

        if event.button == self._forty_two:
            asyncio.create_task(self.app.action_forty_two())  # type: ignore
