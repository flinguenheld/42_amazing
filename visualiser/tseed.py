from textual.widgets import Input, Label, Button
from textual.containers import ScrollableContainer, HorizontalGroup
from textual.app import ComposeResult
from textual.screen import ModalScreen

from visualiser.ttitle import TTitleSeed
from mazegen.config import Config


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░▀▀█░█▀▀░█▀▀░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀░
class TSeed(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._config: Config = config
        self._seed = Input(
            placeholder="Any text",
            id="seed_input",
        )
        if self._config.seed:
            self._seed.value = self._config.seed

        self._past_seeds = Label(id="seed_history")
        self._past_seeds.border_title = "History"
        self.init_label()
        self._bt_no = Button(
            "No seed", variant="error", classes="option_button"
        )
        self._bt_set = Button(
            "Set seed", variant="primary", classes="option_button"
        )

    def compose(self) -> ComposeResult:
        with ScrollableContainer(classes="layout_options"):
            yield TTitleSeed()
            yield self._seed
            yield self._past_seeds
            with HorizontalGroup(id="option_button_layout"):
                yield self._bt_set
                yield self._bt_no

    # ########################################################################
    # ########################################################### HISTORY ####
    def init_label(self) -> None:
        if not self._config.past_seeds:
            self._past_seeds.content = "Empty"
        else:
            text = ""
            for seed in reversed(self._config.past_seeds[-10:]):
                text += f"{seed}\n"
            self._past_seeds.update(text)

    # ########################################################################
    # ################################################### BUTTON PRESSED #####
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Dismiss the seed if there's one or None"""

        if event.button == self._bt_set:
            if self._seed.value:
                self._config.update_seed(self._seed.value)
                self.dismiss(self._seed.value)
            else:
                self.dismiss(None)

        elif event.button == self._bt_no:
            self._config.clear_seed()
            self.dismiss(None)
