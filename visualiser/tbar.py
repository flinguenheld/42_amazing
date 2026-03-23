from textual.reactive import reactive
from textual.containers import HorizontalGroup
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label

from mazegen.config import Config


class TBar(Static):
    def __init__(self, config: Config):

        super().__init__()
        self._config = config
        self._tsize = Label("Size:", classes="bar_label")
        self._talgo = Label("Algo:", classes="bar_label")
        self._tperfect = Label("Perfect", classes="bar_label")
        self._toutput_file = Label("Output file:", classes="bar_label")
        self._tseed = Label("Seed:", classes="bar_label bar_golden_colour")

        self.refresh_values()

    # ########################################################################
    # ########################################################## COMPOSE #####
    def compose(self) -> ComposeResult:
        with HorizontalGroup(id="bar_layout"):
            yield self._tsize
            yield self._talgo
            yield self._tperfect
            yield self._tseed
            yield self._toutput_file

    # ########################################################################
    # ################################################### REFRESH VALUES #####
    def refresh_values(self) -> None:
        self._tsize.content = (
            f"Size: {self._config.nb_col}/{self._config.nb_row}"
        )
        self._talgo.content = f"Algorithm: {self._config.algo}"

        if not self._config.perfect:
            self._tperfect.add_class("bar_golden_colour")
            self._tperfect.content = f"Loop ratio: {self._config.loop_ratio}"
        else:
            self._tperfect.remove_class("bar_golden_colour")
            self._tperfect.content = "Perfect"

        if not self._config.output_file:
            self._toutput_file.add_class("bar_hide_label")
        else:
            self._toutput_file.remove_class("bar_hide_label")

        if not self._config.output_file:
            self._toutput_file.add_class("bar_hide_label")
        else:
            self._toutput_file.remove_class("bar_hide_label")
            self._toutput_file.content = (
                f"Output file: {self._config.output_file}"
            )

        if not self._config.seed:
            self._tseed.add_class("bar_hide_label")
        else:
            self._tseed.remove_class("bar_hide_label")
            self._tseed.content = f'Seed: "{self._config.seed}"'
