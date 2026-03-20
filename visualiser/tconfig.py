from typing import Tuple
from pydantic import ValidationError

from textual.widget import Widget
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Checkbox, Select
from textual.containers import HorizontalGroup, ScrollableContainer

from mazegen.config import Config
from visualiser.ttitle import TTitleConfig
from visualiser.tmessage import TMessageError

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

        self._width = InputSize(
            "Width:", Config.MIN_SIZE, Config.MAX_SIZE, "Width"
        )
        self._height = InputSize(
            "Height:", Config.MIN_SIZE, Config.MAX_SIZE, "Height"
        )
        self._entry = InputCoordinate(
            "Entry coordinates:", self._config, "X", "Y"
        )
        self._exit = InputCoordinate(
            "Exit coordinates:", self._config, "X", "Y"
        )
        self._algorithm = Select(
            ((algo, algo) for algo in self.ALGORITHMS),
            prompt="Algorithm",
            value=self._config.algo,
            classes="option_select_coordinate_algo",
        )
        self._perfect = Checkbox(
            classes="option_checkbox", value=self._config.perfect
        )
        self._loop_ratio = Select(
            [(str(i), i) for i in range(0, 101)],
            value=self._config.loop_ratio,
            classes="option_hidden"
            if self._config.perfect
            else "option_select_ratio",
        )
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
    # ############################################# READ EXISTING CONFIG #####
    def read_existing_config(self) -> None:
        try:
            self._height.set_value(self._config.nb_row)
            self._width.set_value(self._config.nb_col)
            self._entry.set_value(self._config.entry)
            self._exit.set_value(self._config.exit)
            self._algorithm.value = self._config.algo
            self._perfect.value = self._config.perfect
            self._algorithm.refresh(layout=True)

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
                "ALGO": self._algorithm.value,
                "PERFECT": self._perfect.value,
                "LOOP_RATIO": self._loop_ratio.value
                if self._loop_ratio.value != Select.NULL
                else 100,
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
    # ########################################################## COMPOSE #####
    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="layout_options"):
            yield TTitleConfig()
            yield self._width
            yield self._height
            yield self._entry
            yield self._exit
            with HorizontalGroup():
                yield Label("Algorithm:", classes="option_label")
                yield self._algorithm
            with HorizontalGroup():
                yield Label("Perfect:", classes="option_label")
                yield self._perfect
            with HorizontalGroup():
                yield Label("Loop Ratio:", classes="option_label")
                yield self._loop_ratio

            with HorizontalGroup(id="option_button_layout"):
                yield self._bt_cancel
                yield self._bt_update
                yield self._bt_save

    # ########################################################################
    # ################################################### BUTTON PRESSED #####
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self._bt_cancel:
            self.app.pop_screen()

        elif event.button == self._bt_update:
            if self._update_config():
                self.app.pop_screen()

        elif event.button == self._bt_save:
            if self._save_config():
                self.app.pop_screen()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox == self._perfect:
            if self._perfect.value:
                self._loop_ratio.classes = "option_hidden"
            else:
                self._loop_ratio.classes = "option_select_ratio"


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░█░█░▀█▀░░░█▀▀░▀█▀░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░█░█░░█░░░░▀▀█░░█░░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class InputSize(Widget):
    def __init__(self, title: str, min: int, max: int, prompt: str):
        super().__init__(classes="option_inputs")
        self._max = max
        self._title = title
        self._prompt = prompt
        self._input = Select(
            ((str(algo), algo) for algo in range(min, self._max)),
            prompt=self._prompt,
            value=5,
            classes="option_select_size",
        )

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label(self._title, classes="option_label")
            yield self._input

    def set_value(self, value: int) -> None:
        if value >= 5 and value <= self._max:
            self._input.value = value

    def get_value(self) -> int:
        return int(self._input.value)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░█░█░▀█▀░░░█▀▀░█▀█░█▀█░█▀▄░█▀▄░▀█▀░█▀█░█▀█░▀█▀░█▀▀
# ░░░░░░░░░░░░░░░░█░░█░█░█▀▀░█░█░░█░░░░█░░░█░█░█░█░█▀▄░█░█░░█░░█░█░█▀█░░█░░█▀▀
# ░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀
class InputCoordinate(Widget):
    def __init__(self, title: str, config: Config, prompt_one: str, prompt_two: str):
        super().__init__(classes="option_inputs")
        self._max_x = config.nb_col
        self._max_y = config.nb_row
        self._title = title
        self._x = Select(
            ((str(algo), algo) for algo in range(0, self._max_x)),
            prompt=prompt_one,
            value=0,
            classes="option_select_coordinate",
        )
        self._y = Select(
            ((str(algo), algo) for algo in range(0, self._max_y)),
            prompt=prompt_two,
            value=0,
            classes="option_select_coordinate",
        )

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label(self._title, classes="option_label")
            yield self._x
            yield self._y

    def set_value(self, values: Tuple[int, int]) -> None:
        if 0 <= values[0] <= self._max_x and 0 <= values[1] <= self._max_y:
            self._x.value = values[1]
            self._y.value = values[0]

    def get_value(self) -> Tuple[int, int]:
        """!! Values are reversed to fit (row,col) instead of (x,y) !!"""
        return (self._y.value, self._x.value)
