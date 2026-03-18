from textual.layout import Layout
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button
from textual.containers import Vertical, Center


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀
class TMessage(ModalScreen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
        ("enter", "app.pop_screen", "Pop screen"),
        ("space", "app.pop_screen", "Pop screen"),
    ]

    def __init__(self, title: str, message: str, layout_class: str) -> None:
        super().__init__()
        self._bt_close = Button(
            "Ok", variant="primary", classes="message_button"
        )
        self._title = Label(title, classes="message_title")
        self._message = Label(message, classes="message_label")
        self._layout = Vertical(id="message_layout_base", classes=layout_class)

    # ########################################################################
    # ############################################################ MOUNT #####
    def compose(self) -> ComposeResult:
        with self._layout:
            yield self._title
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
        super().__init__(
            """
██████ █████▄  █████▄  ▄████▄ █████▄  
██▄▄   ██▄▄██▄ ██▄▄██▄ ██  ██ ██▄▄██▄ 
██▄▄▄▄ ██   ██ ██   ██ ▀████▀ ██   ██ """,
            message,
            "message_layout_error",
        )


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀░░░█░█░█▀█░█▀▄░█▀█░▀█▀░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀░░░█▄█░█▀█░█▀▄░█░█░░█░░█░█░█░█
# ░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀
class TMessageWarning(TMessage):
    def __init__(self, message: str):
        super().__init__(
            """
██     ██ ▄████▄ █████▄  ███  ██ ██ ███  ██  ▄████  
██ ▄█▄ ██ ██▄▄██ ██▄▄██▄ ██ ▀▄██ ██ ██ ▀▄██ ██  ▄▄▄ 
 ▀██▀██▀  ██  ██ ██   ██ ██   ██ ██ ██   ██  ▀███▀   """,
            message,
            "message_layout_warning",
        )


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀░░░█▀▀░█░█░█▀▀░█▀▀░█▀▀░█▀▀░█▀▀
# ░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀░░░▀▀█░█░█░█░░░█░░░█▀▀░▀▀█░▀▀█
# ░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class TMessageSuccess(TMessage):
    def __init__(self, message: str):
        super().__init__(
            """
▄█████ ██  ██ ▄█████ ▄█████ ██████ ▄█████ ▄█████ 
▀▀▀▄▄▄ ██  ██ ██     ██     ██▄▄   ▀▀▀▄▄▄ ▀▀▀▄▄▄ 
█████▀ ▀████▀ ▀█████ ▀█████ ██▄▄▄▄ █████▀ █████▀ """,
            message,
            "message_layout_success",
        )
