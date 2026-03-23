from pydantic import ValidationError

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.containers import HorizontalGroup, ScrollableContainer

from mazegen.config import Config
from visualiser.ttitle import TTitleConfig
from visualiser.tmessage import TMessageError
from visualiser.tconfig_widgets import (
    TInputCoordinate,
    TInputPerfect,
    TInputSize,
    TInputStr,
    TAlgoSelection,
)

import sys


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█░█░█░█░█▀▀░░█░░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀
class TConfig(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]
    ALGORITHMS = ["Wilson", "DFS"]

    def __init__(self, config: Config):
        super().__init__()
        self._config: Config = config

        self._width = TInputSize(
            "Width:", Config.MIN_SIZE, Config.MAX_SIZE, "Width"
        )
        self._height = TInputSize(
            "Height:", Config.MIN_SIZE, Config.MAX_SIZE, "Height"
        )
        self._entry = TInputCoordinate(
            "Entry coordinates:", Config.MAX_SIZE, "X", "Y"
        )
        self._exit = TInputCoordinate(
            "Exit coordinates:", Config.MAX_SIZE, "X", "Y"
        )
        self._algorithm = TAlgoSelection(self.ALGORITHMS)
        self._perfect_ratio = TInputPerfect()
        self._output_file = TInputStr(
            "Output file:", placeholder="output file"
        )

        # --
        self._bt_cancel = Button(
            "Cancel", variant="default", classes="option_button"
        )
        self._bt_update = Button(
            "Update", variant="primary", classes="option_button"
        )
        self._bt_save = Button(
            "Save file", variant="error", classes="option_button"
        )

    # ########################################################################
    # ############################################################ MOUNT #####
    def on_mount(self) -> None:
        self.read_existing_config()

    # ########################################################################
    # ########################################################## COMPOSE #####
    def compose(self) -> ComposeResult:
        with ScrollableContainer(classes="layout_options"):
            yield TTitleConfig()
            yield self._width
            yield self._height
            yield self._entry
            yield self._exit
            yield self._algorithm
            yield self._perfect_ratio
            yield self._output_file

            with HorizontalGroup(id="option_button_layout"):
                yield self._bt_cancel
                yield self._bt_update
                yield self._bt_save

    # ########################################################################
    # ############################################# READ EXISTING CONFIG #####
    def read_existing_config(self) -> None:
        try:
            self._height.set_value(self._config.nb_row)
            self._width.set_value(self._config.nb_col)
            self._entry.set_value(self._config.entry)
            self._exit.set_value(self._config.exit)
            self._algorithm.set_value(self._config.algo)
            self._perfect_ratio.set_value(
                self._config.perfect, self._config.loop_ratio
            )
            self._output_file.set_value(self._config.output_file)

        except ValidationError as e:
            # Can't append normally...
            self.app.push_screen(TMessageError(f"{e.errors()[0]['msg']}"))
            self.app.exit()

    # ########################################################################
    # #################################################### UPDATE CONFIG #####
    def _update_config(self) -> bool:
        try:
            new_config_values = {
                "WIDTH": self._width.get_value(),
                "HEIGHT": self._height.get_value(),
                "ENTRY": self._entry.get_value(),
                "EXIT": self._exit.get_value(),
                "ALGO": self._algorithm.get_value(),
                "PERFECT": self._perfect_ratio.get_perfect(),
                "LOOP_RATIO": self._perfect_ratio.get_ratio(),
                "OUTPUT_FILE": self._output_file.get_value(),
            }
            new_config = Config.model_validate(new_config_values)

        except ValidationError as e:
            self.app.push_screen(TMessageError(f"{e.errors()[0]['msg']}"))
            return False

        else:
            self._config.__dict__.update(new_config.__dict__)
            return True

    # ########################################################################
    # ###################################################### SAVE CONFIG #####
    def _save_config(self) -> bool:
        if not self._update_config():
            return False
        conf = self._config.model_dump(by_alias=True)
        res = ""
        for k, v in conf.items():
            if v:
                if isinstance(v, tuple):
                    res = f"{res}{k}={v[1]},{v[0]}\n"
                else:
                    res = f"{res}{k}={v}\n"
        with open(sys.argv[1], "w") as fd:
            fd.write(res)
        return True

    # ########################################################################
    # ################################################### BUTTON PRESSED #####
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self._bt_cancel:
            self.dismiss(False)

        elif event.button == self._bt_update:
            if self._update_config():
                self.dismiss(True)

        elif event.button == self._bt_save:
            if self._save_config():
                self.dismiss(True)
