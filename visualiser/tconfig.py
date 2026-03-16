from typing import Tuple
from pydantic import ValidationError

from textual.widget import Widget
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Checkbox, Select
from textual.containers import HorizontalGroup, ScrollableContainer

from mazegen.config import Config
from visualiser.ttitle import TTitleConfig
from config.config_parser import ConfigParser

# TODO: READ OPTIONS
# TODO: SAVE OPTIONS
# TODO: GET & UPDATE THE OBJECT
# TODO: CHECK THE VALUES !
# TODO: CREATE TERROR WIDGET
# TODO: ADD DEFAULT THEME


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█░█░█░█░█▀▀░░█░░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀
class TConfig(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]
    ALGORITHMS = ["Wilson", "DFS"]
    MAX_SIZE = 200

    # TODO: ADD A VARIABLE
    PATH = "config_test.txt"

    def __init__(self, config: Config):
        super().__init__()
        self._config: Config = config

        self._width = InputSize("Width:", self.MAX_SIZE, "Width")
        self._height = InputSize("Height:", self.MAX_SIZE, "Height")
        self._entry = InputCoordinate(
            "Entry coordinates:", self.MAX_SIZE - 1, "X", "Y"
        )
        self._exit = InputCoordinate(
            "Exit coordinates:", self.MAX_SIZE - 1, "X", "Y"
        )
        self._algorithm = Select(
            ((algo, algo) for algo in self.ALGORITHMS),
            prompt="Algorithm",
            value=self.ALGORITHMS[0],
            classes="option_select_coordinate_algo",
        )
        self._perfect = Checkbox(classes="option_checkbox")
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
    def read_existing_config(self):
        try:
            self._height.set_value(self._config.nb_row)
            self._width.set_value(self._config.nb_col)
            self._entry.set_value(self._config.entry)
            self._exit.set_value(self._config.exit)
            self._algorithm.value = "DFS"
            self._algorithm.refresh(layout=True)

        except ValidationError as e:
            pass
            # TODO: ADD TESTS ??????
            # cprint("Config file error", file=sys.stderr, color="red")
            # for err in e.errors():
            #     cprint(f"  - {err['msg']}", file=sys.stderr, color="red")
            # cprint(usage(), file=sys.stderr, color="yellow")

        # except FileNotFoundError:
        #     cprint("Config file not found", file=sys.stderr, color="red")
        #     cprint(usage(), file=sys.stderr, color="yellow")

    # ########################################################################
    # #################################################### UPDATE CONFIG #####
    def _update_config(self):
        # try:
        new_config_values = {
            "WIDTH": self._width.get_value(),
            "HEIGHT": self._height.get_value(),
            "ENTRY": self._entry.get_value(),
            "EXIT": self._exit.get_value(),
            "ALGO": self._algorithm.value,
        }

        new_config = Config.model_validate(new_config_values)
        self._config.nb_col = new_config.nb_col
        self._config.nb_row = new_config.nb_row
        self._config.entry = new_config.entry
        self._config.exit = new_config.exit
        self._config.algo = new_config.algo

        # except ValidationError as e:
        #     pass
        # TODO: ADD TESTS ??????
        # cprint("Config file error", file=sys.stderr, color="red")
        # for err in e.errors():
        #     cprint(f"  - {err['msg']}", file=sys.stderr, color="red")
        # cprint(usage(), file=sys.stderr, color="yellow")

        # except FileNotFoundError:
        #     cprint("Config file not found", file=sys.stderr, color="red")
        #     cprint(usage(), file=sys.stderr, color="yellow")

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
            self._update_config()
            self.app.pop_screen()
        elif event.button == self._bt_save:
            self.app.exit()


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░█░█░▀█▀░░░█▀▀░▀█▀░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░█░█░░█░░░░▀▀█░░█░░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class InputSize(Widget):
    def __init__(self, title: str, max: int, prompt: str):
        super().__init__(classes="option_inputs")
        self._max = max
        self._title = title
        self._prompt = prompt
        self._input = Select(
            ((str(algo), algo) for algo in range(5, self._max)),
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
    def __init__(self, title: str, max: int, prompt_one: str, prompt_two: str):
        super().__init__(classes="option_inputs")
        self._max = max
        self._title = title
        self._x = Select(
            ((str(algo), algo) for algo in range(0, self._max)),
            prompt=prompt_one,
            value=0,
            classes="option_select_coordinate",
        )
        self._y = Select(
            ((str(algo), algo) for algo in range(0, self._max)),
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
        if (
            values[0] >= 5
            and values[0] <= self._max
            and values[1] >= 5
            and values[1] <= self._max
        ):
            self._x.value = values[0]
            self._y.value = values[1]

    def get_value(self) -> Tuple[int, int]:
        return (self._x.value, self._y.value)
