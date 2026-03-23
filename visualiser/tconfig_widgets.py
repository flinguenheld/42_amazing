from typing import Tuple, Optional, List

from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, Select, Input, Switch
from textual.containers import HorizontalGroup


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░█░█░▀█▀░░░█▀▀░▀█▀░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░█░█░░█░░░░▀▀█░░█░░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class TInputSize(Widget):
    def __init__(self, title: str, min: int, max: int, prompt: str):
        super().__init__(classes="option_inputs")
        self._max = max
        self._title = title
        self._input = Select(
            ((str(algo), algo) for algo in range(min, self._max)),
            prompt=prompt,
            value=5,
        )

    def compose(self) -> ComposeResult:
        with HorizontalGroup(classes="option_field_layout"):
            yield Label(self._title, classes="option_label")
            yield self._input

    def set_value(self, value: int) -> None:
        if value >= 5 and value <= self._max:
            self._input.value = value

    def get_value(self) -> int:
        return int(str(self._input.value))


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░█░█░▀█▀░░░█▀█░█▀▀░█▀▄░█▀▀░█▀▀░█▀▀░▀█▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░█░█░░█░░░░█▀▀░█▀▀░█▀▄░█▀▀░█▀▀░█░░░░█░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░░▀░░░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░▀░
class TInputPerfect(Widget):
    def __init__(self) -> None:
        super().__init__(classes="option_inputs")
        self._perfect = Switch(classes="option_switch")
        self._loop_ratio = Select(
            [(f"Ratio: {i}", i) for i in range(0, 101)],
            prompt="Ratio",
            value=100,
        )

    def compose(self) -> ComposeResult:
        with HorizontalGroup(classes="option_field_layout"):
            yield Label("Perfect:", classes="option_label")
            yield self._perfect
            yield self._loop_ratio

    def on_switch_changed(self, event: Switch.Changed) -> None:
        if self._perfect.value:
            self._loop_ratio.add_class("option_switch_hidden")
        else:
            self._loop_ratio.remove_class("option_switch_hidden")

    def set_value(self, perfect: bool, ratio: int) -> None:
        self._perfect.value = perfect
        self._loop_ratio.value = ratio

    def get_ratio(self) -> str:
        return str(self._loop_ratio.value)

    def get_perfect(self) -> bool:
        return bool(self._perfect.value)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░█░█░▀█▀░░░█▀▀░▀█▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░█░█░░█░░░░▀▀█░░█░░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░░▀▀▀░░▀░░▀░▀
class TInputStr(Widget):
    def __init__(self, title: str, placeholder: str):
        super().__init__(classes="option_inputs")
        self._title = title
        self._input = Input(
            placeholder=placeholder,
            classes="option_input_str",
        )

    def compose(self) -> ComposeResult:
        with HorizontalGroup(classes="option_field_layout"):
            yield Label(self._title, classes="option_label")
            yield self._input

    def set_value(self, value: Optional[str]) -> None:
        if value:
            self._input.value = value

    def get_value(self) -> str:
        return str(self._input.value)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░░░█▀▀░█▀█░░░█▀▀░█▀▀░█░░░█▀▀░█▀▀░▀█▀░▀█▀░█▀█░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░░░█░█░█░█░░░▀▀█░█▀▀░█░░░█▀▀░█░░░░█░░░█░░█░█░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀
class TAlgoSelection(Widget):
    def __init__(self, algorithms: List[str]):
        super().__init__(classes="option_inputs")
        self._algorithm = Select(
            ((algo, algo) for algo in algorithms),
            prompt="Algorithm",
        )

    def compose(self) -> ComposeResult:
        with HorizontalGroup(classes="option_field_layout"):
            yield Label("Algorithm:", classes="option_label")
            yield self._algorithm

    def set_value(self, value: Optional[str]) -> None:
        if value:
            self._algorithm.value = value

    def get_value(self) -> str:
        return str(self._algorithm.value)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▀█░█▀█░█░█░▀█▀░░░█▀▀░█▀█░█▀█░█▀▄░█▀▄░▀█▀░█▀█░█▀█░▀█▀░█▀▀
# ░░░░░░░░░░░░░░░░█░░█░█░█▀▀░█░█░░█░░░░█░░░█░█░█░█░█▀▄░█░█░░█░░█░█░█▀█░░█░░█▀▀
# ░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀
class TInputCoordinate(Widget):
    def __init__(self, title: str, max: int, prompt_one: str, prompt_two: str):
        super().__init__(classes="option_inputs")
        self._max_x = max
        self._max_y = max
        self._title = title
        self._x = Select(
            ((str(algo), algo) for algo in range(0, self._max_x)),
            prompt=prompt_one,
            value=0,
        )
        self._y = Select(
            ((str(algo), algo) for algo in range(0, self._max_y)),
            prompt=prompt_two,
            value=0,
        )

    def compose(self) -> ComposeResult:
        with HorizontalGroup(classes="option_field_layout"):
            yield Label(self._title, classes="option_label")
            yield self._x
            yield self._y

    def set_value(self, values: Tuple[int, int]) -> None:
        if 0 <= values[1] <= self._max_x and 0 <= values[0] <= self._max_y:
            self._x.value = values[1]
            self._y.value = values[0]

    def get_value(self) -> Tuple[int, int]:
        """!! Values are reversed to fit (row,col) instead of (x,y) !!"""
        return (self._y.value, self._x.value)
