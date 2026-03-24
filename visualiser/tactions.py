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
            await self.app.run_action("generate_new_maze")

        if event.button == self._start:
            await self.app.run_action("start_new_maze")

        if event.button == self._next_step:
            await self.app.run_action("next_step")

        if event.button == self._build_maze:
            await self.app.run_action("animate")

        if event.button == self._stop_animation:
            await self.app.run_action("stop_animations")

        if event.button == self._restart_player:
            await self.app.run_action("restart_player")

        if event.button == self._solution:
            await self.app.run_action("solution")

        if event.button == self._solution_deactivate:
            await self.app.run_action("solution_deactivate")

        if event.button == self._forty_two:
            await self.app.run_action("forty_two")
