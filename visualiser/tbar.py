from textual.events import Click
from textual import work
from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import HorizontalGroup

from mazegen.config import Config
from visualiser.tconfig import TConfig
from visualiser.tseed import TSeed


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀░░▀░▀░▀░▀
class TBar(Static):
    def __init__(self, config: Config) -> None:

        super().__init__()
        self._config = config
        self._tsize = Label("Size:", classes="bar_label")
        self._talgo = Label("Algo:", classes="bar_label")
        self._tperfect = Label("Perfect", classes="bar_label")
        self._toutput_file = Label("Output file:", classes="bar_label")
        self._tseed = Label("Seed:", classes="bar_label")

    # ########################################################################
    # ############################################################ CLICK #####
    @work
    async def on_click(self, event: Click) -> None:
        if event.widget == self._tseed:
            await self.app.push_screen_wait(TSeed(self._config))
        else:
            await self.app.push_screen_wait(TConfig(self._config))

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
        self._tsize.update(
            f"Size: {self._config.nb_col}/{self._config.nb_row}"
        )
        self._talgo.update(f"Algorithm: {self._config.algo}")

        if not self._config.perfect:
            self._tperfect.remove_class("bar_green_colour")
            self._tperfect.add_class("bar_accent_colour")
            self._tperfect.update(f"Loop ratio: {self._config.loop_ratio}")
        else:
            self._tperfect.add_class("bar_green_colour")
            self._tperfect.remove_class("bar_accent_colour")
            self._tperfect.update("Perfect")

        if not self._config.output_file:
            self._toutput_file.add_class("bar_hide_label")
        else:
            self._toutput_file.remove_class("bar_hide_label")

        if not self._config.output_file:
            self._toutput_file.add_class("bar_hide_label")
        else:
            self._toutput_file.remove_class("bar_hide_label")
            self._toutput_file.update(
                f"Output file: {self._config.output_file}"
            )

        if not self._config.seed:
            self._tseed.remove_class("bar_golden_colour")
            self._tseed.update("No seed")
        else:
            self._tseed.add_class("bar_golden_colour")
            self._tseed.update(f'Seed: "{self._config.seed}"')
