from textual.widget import Widget
from textual import on
from textual.widgets import Label, Button, Checkbox, Select
from textual.containers import (
    HorizontalGroup,
    VerticalScroll,
)
from textual.app import ComposeResult
from textual.screen import ModalScreen
from visualiser.ttitle import TTitleOption

# TODO: READ OPTIONS
# TODO: SAVE OPTIONS
# TODO: GET & UPDATE THE OBJECT
# TODO: CHECK THE VALUES !


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░▀█▀░▀█▀░█▀█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░░█░░░█░░█░█░█░█░▀▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░░░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀
class TOptions(ModalScreen):
    ALGORITHMS = ["Wilson", "DFS"]
    MAX_SIZE = 150

    def __init__(self):
        super().__init__()

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
        self._cancel = Button(
            "Cancel", variant="primary", classes="option_button"
        )
        self._save = Button("Save", variant="error", classes="option_button")

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="layout_options"):
            yield TTitleOption()
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
                yield self._cancel
                yield self._save

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.app.exit()
        else:
            self.app.pop_screen()


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

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label(self._title, classes="option_label")
            yield Select(
                ((str(algo), algo) for algo in range(0, self._max)),
                prompt=self._prompt,
                value=0,
                classes="option_select_size",
            )


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░█░█░▀█▀░░░█▀▀░█▀█░█▀█░█▀▄░█▀▄░▀█▀░█▀█░█▀█░▀█▀░█▀▀
# ░░░░░░░░░░░░░░░░█░░█░█░█▀▀░█░█░░█░░░░█░░░█░█░█░█░█▀▄░█░█░░█░░█░█░█▀█░░█░░█▀▀
# ░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀
class InputCoordinate(Widget):
    def __init__(self, title: str, max: int, prompt_one: str, prompt_two: str):
        super().__init__(classes="option_inputs")
        self._max = max
        self._title = title
        self._prompt_one = prompt_one
        self._prompt_two = prompt_two

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label(self._title, classes="option_label")
            yield Select(
                ((str(algo), algo) for algo in range(0, self._max)),
                prompt=self._prompt_one,
                value=0,
                classes="option_select_coordinate",
            )
            yield Select(
                ((str(algo), algo) for algo in range(0, self._max)),
                prompt=self._prompt_two,
                value=0,
                classes="option_select_coordinate",
            )
