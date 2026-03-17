from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button
from textual.containers import Vertical, Center


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀
class TMessage(ModalScreen):
    # TODO: Fix BINDNIGS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
        ("enter", "app.pop_screen", "Pop screen"),
        ("space", "app.pop_screen", "Pop screen"),
    ]

    def __init__(self, message: str, type: str) -> None:
        super().__init__()
        self._layout = Vertical(id="layout_message")
        match type:
            case "error":
                self._layout.add_class("layout_message_error")
            case "warning":
                self._layout.add_class("layout_message_warning")
            case _:
                self._layout.add_class("layout_message_success")

        self._message = Label(message, classes="message_label")
        self._bt_close = Button(
            "Ok", variant="primary", classes="message_button"
        )

    # ########################################################################
    # ############################################################ MOUNT #####
    def compose(self) -> ComposeResult:
        with self._layout:
            yield self._message
            with Center():
                yield self._bt_close

    # ########################################################################
    # ################################################### BUTTON PRESSED #####
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self._bt_close:
            self.app.pop_screen()


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
class TMessageError(TMessage):
    def __init__(self, message: str):
        super().__init__(message, "error")


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀░░░█░█░█▀█░█▀▄░█▀█░▀█▀░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀░░░█▄█░█▀█░█▀▄░█░█░░█░░█░█░█░█
# ░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀
class TMessageWarning(TMessage):
    def __init__(self, message: str):
        super().__init__(message, "warning")


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀░░░█▀▀░█░█░█▀▀░█▀▀░█▀▀░█▀▀░█▀▀
# ░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀░░░▀▀█░█░█░█░░░█░░░█▀▀░▀▀█░▀▀█
# ░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class TMessageSuccess(TMessage):
    def __init__(self, message: str):
        super().__init__(message, "success")
